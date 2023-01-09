from guizero import *
from datetime import datetime
import dateutil.parser as p
import os
import time

app = App(title="app", bg="black")
app.full_screen = True
tsultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==1{print $1; exit}' | cut -c2- | sed 's/.$//'"
tspenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $1}' | awk 'NR==2{print $1; exit}' | cut -c2- | sed 's/.$//'"
valueultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==1{print $1; exit}'"
valuepenultimo="curl -sX GET \"https://HOST-NIGHTSCOUT/api/v1/entries?count=2&token=TOKEN\" | awk '{print $3}' | awk 'NR==2{print $1; exit}'"

snooze=0
alarm=0

def glice():

	global snooze #prendo le variabili globali
	global alarm

#	orario attuale e minuti da ultima lettura

	ultimo=os.popen(tsultimo).read() #timestamp ultima lettura

	nowraw=datetime.now() #timestamp standard di adesso
	now=nowraw.strftime("%Y-%m-%dT%H:%M:%SZ") #timestamp con Z di adesso
	time=nowraw.strftime("%H:%M") #ora e minuti attuali in formato TS
	orario=f"{time}" #stringa con ora attuale

	diff=((p.parse(now)-p.parse(ultimo)).total_seconds()/60)-60 #differenza tra adesso e ultima lettua (con Z)

	if int(diff)==0: #creazione stringa dei minuti trascorsi da ultima lettura
		lastage=f"adesso"
	elif int(diff)==1:
		intdiff=int(diff)
		lastage=f"{intdiff} minuto fa"
	else:
		intdiff=int(diff)
		lastage=f"{intdiff} minuti fa"

#	valore di glucosio e delta con precedente

	ultimobg=int(os.popen(valueultimo).read()) #ultima lettura glucosio
	lastbg=f"{ultimobg}" #stringra ultima lettura glucosio

	if int(lastbg)>=180: #se alta o bassa assegnazione colore al testo icona dipendente da snooze
		lastbggui.text_color=f"yellow"
		alarm=1
		if snooze==1:
			imgalarm.value=f"/home/matteo/glice/bellsnooze.png"
		else:
			imgalarm.value=f"/home/matteo/glice/bell.png"
	elif int(lastbg)<70:
		alarm=1
		lastbggui.text_color=f"red"
		if snooze==1:
			imgalarm.value=f"/home/matteo/glice/bellsnooze.png"
		else:
			imgalarm.value=f"/home/matteo/glice/bell.png"
	else:
		alarm=0
		lastbggui.text_color=f"green"
		imgalarm.value=f"/home/matteo/glice/bellblack.png"
		snooze=0
	penultimobg=os.popen(valuepenultimo).read() #penultima lettura glucosio
	delta=int(ultimobg)-int(penultimobg) #calcolo differenza ultima e penultima lettura
	if delta>=0: #aggiungi di un + se differenza positiva
		delta=f"+{delta}"
	lastdelta=f"{delta}" #stringa valore di differenza

#	dichiarazioni per GUI (valori e immagini)

	diffgui.value=f"{lastage}"
	timegui.value=f"{orario}"
	lastbggui.value=f"{lastbg}"
	lastdeltagui.value=f"{lastdelta}"
	if int(delta)>=-5 and int(delta)<=5:
		imgcur.value=f"/home/matteo/glice/stable.png"
	elif int(delta)>5 and int(delta)<=10:
		imgcur.value="/home/matteo/glice/up.png"
	elif int(delta)>10 and int(delta)<=19:
		imgcur.value="/home/matteo/glice/upup.png"
	elif int(delta)>19:
		imgcur.value="/home/matteo/glice/upupup.png"
	elif int(delta)<-5 and int(delta)>=-10:
		imgcur.value="/home/matteo/glice/down.png"
	elif int(delta)<-10 and int(delta)>=-19:
		imgcur.value="/home/matteo/glice/downdown.png"
	elif int(delta)<-19:
		imgcur.value="/home/matteo/glice/downdowndown.png"
	else:
		imgcur.value="/home/matteo/glice/arrowblack.png"

	return [snooze, alarm] #mando le varibili globali

def button1(): #snooze
	global snooze
	global alarm
	if alarm==0:
		pass
	else:
		imgalarm.value=f"/home/matteo/glice/bellsnooze.png"
		snooze=1
	return [snooze, alarm]

def button2(): #bottone di uscita
	quit()

app.repeat(5000, glice)

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

glice()
app.display()

