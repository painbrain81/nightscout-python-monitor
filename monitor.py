from guizero import *
from datetime import datetime
import dateutil.parser as p
import os
import time

#parametrizzazione principale

user="matteo"
folder="nightscout-python-monitor"
lvlup=180 #livello alta glicemia
lvldown=70 #livello bassa glicemia
sogliap1=5 #stabile
sogliap2=10 #leggera salita
sogliap3=19 #salita e salita rapida
sogliam1=-5 #stabile
sogliam2=-10 #leggera discesa
sogliam3=-19 #discesa e discesa rapida
ritardobg=15 #soglia oltre la quale sparisce il valore di glicemia
minutioralegale=60 #60 per ora solare, 120 per ora legale
refresh=5000 #in millisecondi

app = App(title="app", bg="black")
app.full_screen = True

#sostituire HOST-NIGHTSCOUT e TOKEN con i propri del proprio nightscout

tsultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==1{print $1; exit}' | cut -c2- | sed 's/.$//'"
tspenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==2{print $1; exit}' | cut -c2- | sed 's/.$//'"
valueultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==1{print $1; exit}'"
valuepenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==2{print $1; exit}'"
oralinux='date +"%s"'

#inizializzazione parametri globali

delay=300
snooze=0
alarm=0
alarmon=0
lastalarm=0

def glice():

	global snooze #prendo le variabili globali
	global alarm
	global alarmon
	global lastalarm
	global delay

#	orario attuale e minuti da ultima lettura
	print("----------")
	ultimo=os.popen(tsultimo).read() #timestamp ultima lettura

	nowraw=datetime.now() #timestamp standard di adesso
	now=nowraw.strftime("%Y-%m-%dT%H:%M:%SZ") #timestamp con Z di adesso
	time=nowraw.strftime("%H:%M") #ora e minuti attuali in formato TS
	orario=f"{time}" #stringa con ora attuale
	print("orario "+orario)
	diff=((p.parse(now)-p.parse(ultimo)).total_seconds()/60)-minutioralegale #differenza tra adesso e ultima lettua (con Z)

	if int(diff)==0: #creazione stringa dei minuti trascorsi da ultima lettura
		lastage=f"adesso"
	elif int(diff)==1:
		intdiff=int(diff)
		lastage=f"{intdiff} minuto fa"
	else:
		intdiff=int(diff)
		lastage=f"{intdiff} minuti fa"
	print(lastage)
#	valore di glucosio e delta con precedente

	ultimobg=int(os.popen(valueultimo).read()) #ultima lettura glucosio
	print("lastbg "+str(ultimobg))
	if int(diff)>ritardobg:
		lastbg=f"---"
		print("ultimo valore oltre 15 min")
		lastbggui.text_color="gray"
	else:
		lastbg=f"{ultimobg}" #stringra ultima lettura glucosio

		adesso=os.popen(oralinux).read() #il prossimo if è la gestione del delay degli allarmi
		if alarm==0 and (int(lastbg)>=lvlup or int(lastbg)<lvldown):
			alarmon=os.popen(oralinux).read()
			lastalarm=os.popen(oralinux).read()
			suona()
			print("attivazione sirena")
		elif alarm==1 and (int(lastbg)>=lvlup or int(lastbg)<lvldown):
			diffalarm=int(adesso)-int(lastalarm)
			if int(diffalarm)>delay:
				suona()
				print("ripetizione sirena")
				lastalarm=os.popen(oralinux).read()
			else:
				pass
		else:
			alarmon=0
			lastalarm=0
			delay=300
			print("spegnimento allarme")

		if int(lastbg)>=lvlup: #se alta o bassa assegnazione colore al testo icona e gestione allarmi
			lastbggui.text_color=f"yellow"
			alarm=1
			print("allarme attivo high")
			if snooze==1:
				imgalarm.value=f"/home/{user}/{folder}/bellsnooze.png"
			else:
				imgalarm.value=f"/home/{user}/{folder}/bell.png"
		elif int(lastbg)<lvldown:
			alarm=1
			print("allarme attivo low")
			lastbggui.text_color=f"red"
			if snooze==1:
				imgalarm.value=f"/home/{user}/{folder}/bellsnooze.png"
			else:
				imgalarm.value=f"/home/{user}/{folder}/bell.png"
		else:
			alarm=0
			print("allarme disattivato")
			lastbggui.text_color=f"green"
			imgalarm.value=f"/home/{user}/{folder}/bellblack.png"
			snooze=0
	penultimobg=os.popen(valuepenultimo).read() #penultima lettura glucosio
	delta=int(ultimobg)-int(penultimobg) #calcolo differenza ultima e penultima lettura
	if delta>=0: #aggiungi di un + se differenza positiva
		delta=f"+{delta}"
	lastdelta=f"{delta}" #stringa valore di differenza
	print("delta "+lastdelta)
#	dichiarazioni per GUI (valori e immagini)

	diffgui.value=f"{lastage}"
	timegui.value=f"{orario}"
	lastbggui.value=f"{lastbg}"
	lastdeltagui.value=f"{lastdelta}"
	if int(delta)>=sogliam1 and int(delta)<=sogliap1:
		imgcur.value=f"/home/{user}/{folder}/stable.png"
		print("stabile")
	elif int(delta)>sogliap1 and int(delta)<=sogliap2:
		imgcur.value=f"/home/{user}/{folder}/up.png"
		print("up")
	elif int(delta)>sogliap2 and int(delta)<=sogliap3:
		imgcur.value=f"/home/{user}/{folder}/upup.png"
		print("upup")
	elif int(delta)>sogliap3:
		imgcur.value=f"/home/{user}/{folder}/upupup.png"
		print("upupup")
	elif int(delta)<sogliam1 and int(delta)>=sogliam2:
		imgcur.value=f"/home/{user}/{folder}/down.png"
		print("down")
	elif int(delta)<sogliam2 and int(delta)>=sogliam3:
		imgcur.value=f"/home/{user}/{folder}/downdown.png"
		print("downdown")
	elif int(delta)<sogliam3:
		imgcur.value=f"/home/{user}/{folder}/downdowndown.png"
		print("downdowndown")
	else:
		imgcur.value=f"/home/{user}/{folder}/arrowblack.png"
		print("freccia nera")

	print("delay "+str(delay))
	print("finito")
	return [snooze, alarm, alarmon, lastalarm, delay] #restituisco le varibili globali

def suona(): #implementare una riproduzione di un suono
	print("sirena!")
	pass

def button1(): #snooze
	global snooze
	global alarm
	global delay
	if alarm==0:
		delay=300
		print("snooze senza allarmi")
	else:
		imgalarm.value=f"/home/{user}/{folder}/bellsnooze.png"
		delay=1800
		snooze=1
		print("snooze attivo")
	return [snooze, alarm,delay]

def button2(): #bottone di uscita
	print("uscita")
	quit()

app.repeat(refresh, glice)

#blocco glicemia, freccia e delta

bgbox=Box(app, align="top", layout="grid")
lastbggui = Text(bgbox, text="", size=140, grid=[0,0])
space0 = Text(bgbox, text="spazio", grid=[1,0], size=5)
imgcur = Picture(bgbox, grid=[2,0])
space1 = Text(bgbox, text="spazio", grid=[3,0], size=5)
lastdeltagui = Text(bgbox, text="", color="white", size=50, grid=[4,0])

#blocco orario e minuti da ultima lettura

timebox=Box(app, align="top", layout="grid")
space2 = Text(timebox, text="spazio", grid=[0,0], size=10)
timegui = Text(timebox, text="", color="white", size=60, grid=[0,1])
space3 =Text(timebox, text="spazio", grid=[1,1], size=20)
diffgui = Text(timebox, text="", color="white", size=30, grid=[2,1])

#blocco pulsanti

buttonbox=Box(app, width="fill",  align="bottom")
button1 = PushButton(buttonbox, text="Silenzia", command=button1, align="left")
imgalarm =Picture(buttonbox, align="left")
button2 = PushButton(buttonbox, text="X", command=button2, align="right")
button1.bg = "white"
button2.bg = "gray"
button1.text_size = 40
button2.text_size = 40

app.display()

