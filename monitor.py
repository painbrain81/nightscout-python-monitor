from guizero import *
from datetime import datetime
import dateutil.parser as p
import os
import time

#parametrizzazione principale

user="matteo" #utente di sistema dove risiede il programma
folder="glice" #cartella dove risiede il programma, necessariamente nella root dell'utente
lvlup=180 #livello alta glicemia
lvldown=70 #livello bassa glicemia
sogliap1=5 #soglia max stabile
sogliap2=10 #soglia max leggera salita
sogliap3=19 #soglia max salita e oltre √® salita rapida
sogliam1=-5 #soglia minima stabile
sogliam2=-10 #soglia minima leggera discesa
sogliam3=-19 #soglia minima discesa e oltre √® discesa rapida
ritardobg=15 #soglia oltre la quale sparisce il valore di glicemia
minutioralegale=60 #60 per ora solare, 120 per ora legale
refresh=10000 #in millisecondi
tastoexit=False #visibilit√† o meno del tasto di uscita
delayshort=300 #tempo minimo tra gli allarmi
delaylong=1800 #tempo massimo tra gli allarmi dopo lo snooze

app = App(title="app", bg="black")
app.full_screen = True

#sostituire HOST-NIGHTSCOUT e TOKEN con i propri del proprio nightscout

tsultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==1{print $1; exit}' | cut -c2- | sed 's/.$//'"
tspenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==2{print $1; exit}' | cut -c2- | sed 's/.$//'"
valueultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==1{print $1; exit}'"
valuepenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==2{print $1; exit}'"
oralinux='date +"%s"'

delay=delayshort
snooze=0
alarm=0
alarmon=0
lastalarm=0
mute=0

def glice():

	global snooze #prendo le variabili globali
	global alarm
	global alarmon
	global lastalarm
	global delay
	global delayshort
	global mute

	ultimo=os.popen(tsultimo).read() #timestamp ultima lettura
	nowraw=datetime.now() #timestamp standard di adesso
	now=nowraw.strftime("%Y-%m-%dT%H:%M:%SZ") #timestamp con Z di adesso
	time=nowraw.strftime("%H:%M") #ora e minuti attuali in formato TS
	orario=f"{time}" #stringa con ora attuale
	diff=((p.parse(now)-p.parse(ultimo)).total_seconds()/60)-minutioralegale #differenza tra adesso e ultima lettua (con Z)

	if int(diff)==0: #creazione stringa dei minuti trascorsi da ultima lettura
		lastage=f"adesso"
	elif int(diff)==1:
		intdiff=int(diff)
		lastage=f"{intdiff} minuto fa"
	else:
		intdiff=int(diff)
		lastage=f"{intdiff} minuti fa"


	ultimobg=int(os.popen(valueultimo).read()) #ultima lettura glucosio

	if int(diff)>ritardobg: #ultima lettura oltre il tempo limite
		lastbg=f"---"
		lastbggui.text_color="gray"
	else:
		lastbg=f"{ultimobg}" #stringa ultima lettura glucosio

		adesso=os.popen(oralinux).read() #il prossimo if √® la gestione del delay degli allarmi e l'avvio della sirena
		if alarm==0 and (int(lastbg)>=lvlup or int(lastbg)<lvldown):
			alarmon=os.popen(oralinux).read()
			lastalarm=os.popen(oralinux).read()
			suona()
		elif alarm==1 and (int(lastbg)>=lvlup or int(lastbg)<lvldown):
			diffalarm=int(adesso)-int(lastalarm)
			if int(diffalarm)>delay:
				suona()
				lastalarm=os.popen(oralinux).read()
			else:
				pass
		else:
			alarmon=0
			lastalarm=0
			delay=delayshort
			button1.image=f"/home/{user}/{folder}/alarm5.png"

		if int(lastbg)>=lvlup: #se alta o bassa assegnazione colore al testo icona e gestione allarmi
			lastbggui.text_color=f"yellow"
			alarm=1
			button1.visible=True
		elif int(lastbg)<lvldown:
			alarm=1
			button1.visible=True
			lastbggui.text_color=f"red"
		else:
			alarm=0
			button1.visible=False
			lastbggui.text_color=f"green"
			snooze=0
	penultimobg=os.popen(valuepenultimo).read() #penultima lettura glucosio
	if int(diff)>ritardobg: #ultima lettura oltre il tempo limite
		button1.visible=False
		lastdelta="--"
		delta="--"
		lastdeltagui.text_color="gray"
	else:
		delta=int(ultimobg)-int(penultimobg) #calcolo differenza ultima e penultima lettura
		if delta>=0: #aggiungi di un + se differenza positiva
			delta=f"+{delta}"
		lastdelta=f"{delta}" #stringa valore di differenza
		lastdeltagui.text_color="white"

#	dichiarazioni per GUI (valori e immagini)

	diffgui.value=f"{lastage}"
	timegui.value=f"{orario}"
	lastbggui.value=f"{lastbg}"
	lastdeltagui.value=f"{lastdelta}"
	if delta=="--":
		imgcur.value=f"/home/{user}/{folder}/arrowblack.png"
	elif int(delta)>=sogliam1 and int(delta)<=sogliap1:
		imgcur.value=f"/home/{user}/{folder}/stable.png"
	elif int(delta)>sogliap1 and int(delta)<=sogliap2:
		imgcur.value=f"/home/{user}/{folder}/up.png"
	elif int(delta)>sogliap2 and int(delta)<=sogliap3:
		imgcur.value=f"/home/{user}/{folder}/upup.png"
	elif int(delta)>sogliap3:
		imgcur.value=f"/home/{user}/{folder}/upupup.png"
	elif int(delta)<sogliam1 and int(delta)>=sogliam2:
		imgcur.value=f"/home/{user}/{folder}/down.png"
	elif int(delta)<sogliam2 and int(delta)>=sogliam3:
		imgcur.value=f"/home/{user}/{folder}/downdown.png"
	elif int(delta)<sogliam3:
		imgcur.value=f"/home/{user}/{folder}/downdowndown.png"
	else:
		imgcur.value=f"/home/{user}/{folder}/arrowblack.png"

	return [snooze, alarm, alarmon, lastalarm, delay, mute] #restituisco le varibili globali

def suona(): #sirena
	global mute
	alarmcmd=f"aplay /home/{user}/{folder}/ding.wav"
	if mute==1:
		pass
	else:
		os.popen(alarmcmd)

def button1(): #snooze
	global snooze
	global alarm
	global delay
	global delaylong
	global delayshort
	if alarm==0:
		delay=delayshort
	else:
		button1.image=f"/home/{user}/{folder}/alarm30.png"
		delay=delaylong
		snooze=1
	return [snooze, alarm,delay]

def button2(): #bottone di uscita
	quit()

def button3(): #tasto muto
	global mute
	if mute==0:
		mute=1
		button3.image=f"/home/{user}/{folder}/mute.png"
	else:
		mute=0
		button3.image=f"/home/{user}/{folder}/nomute.png"
	return mute

app.repeat(refresh, glice)

bgbox=Box(app, align="top", layout="grid")
lastbggui = Text(bgbox, text="", size=140, grid=[0,0])
space0 = Text(bgbox, text="spazio", grid=[1,0], size=5)
imgcur = Picture(bgbox, grid=[2,0])
space1 = Text(bgbox, text="spazio", grid=[3,0], size=5)
lastdeltagui = Text(bgbox, text="", color="white", size=50, grid=[4,0])

timebox=Box(app, align="top", layout="grid")
space2 = Text(timebox, text="spazio", grid=[0,0], size=10)
timegui = Text(timebox, text="", color="gray", size=60, grid=[0,1])
space3 =Text(timebox, text="spazio", grid=[1,1], size=20)
diffgui = Text(timebox, text="", color="gray", size=30, grid=[2,1])

buttonbox=Box(app, width="fill",  align="bottom")
button1 = PushButton(buttonbox, command=button1, align="left")
button2 = PushButton(buttonbox, text="X", command=button2, align="right")
button2.visible=tastoexit #tasto di uscita per debug
button2.bg = "gray"
button1.bg = "gray"
button1.image=f"/home/{user}/{folder}/alarm5.png"
button2.text_size = 40
button3 = PushButton(buttonbox, command=button3, align="right")
button3.image=f"/home/{user}/{folder}/nomute.png"
button3.text_size = 40
button3.bg = "gray"

glice()
app.display()
