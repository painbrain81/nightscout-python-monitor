<h2>NOTA: le foto sono della versione vecchia!</h2>

# nightscout-python-monitor
Un monitor in python che si basa su nightscout e GUIZero. 
Hardware necessario un raspberry pi (almeno il 4) e un monitor gpio/hdmi da 5 pollici con touchscreen (questo è quello del prototipo: http://www.waveshare.com/wiki/5inch_HDMI_LCD )

Software necessario Raspberry Pi OS.

<b>Applicazioni necessarie:</b>

sudo apt-get install python3 python3-pip git python3-tk python3-dateutil

sudo pip3 install guizero

Nel file monitor.py bisogna mettere HOST-NIGHTSCOUT e TOKEN relativi al proprio nightscout nelle prime righe nonchè il nome del proprio utente e la cartella (rigorosamente nella cartella root del proprio utente) dove risiede il programma.

L'impaginazione è adeguata per un monitor con risoluzione 800x480.

Il tasto silenzia è attivo se compare un allarme e fa suonare gli allarmi ogni 30 minuti. Se invece viene premuto suona ogni 5 finchè i valori non tornano in range.
La visualizzazione del tasto per uscire è impostabile dai parametri globali.
Se i valori sono più vecchi di 15 minuti (impostabile nei parametri) le scritte diventano tutti trattini e di colore grigio. Si ripristina da solo al primo valore disponibile più recente.

In basso a destra c'è il tasto Muto/Suona per, rispettivamente, spegnere completamente gli allarmi o farglieli gestire in autonomia.

<b>Speaker:</b>
piccolo inciso sullo speaker (ho preso questo: https://it.aliexpress.com/item/1005004442879029.html?spm=a2g0o.order_list.order_list_main.10.5eda36968OiFYM&gatewayAdapt=glo2ita )
per farlo andare senza troppi sbattimenti sul raspberry aprite il file /etc/modprobe.d/raspi-blacklist.conf e ci mettete dentro "blacklist snd_bcm2835" (senza virgolette) e poi aprite il file /lib/modprobe.d/aliases.conf e commentate con un # davanti la riga con scritto "options snd-usb-audio index=-2" (anche qui senza virgolette) e poi riavviate il rapsberry. Praticamente così facendo escludete tutti gli audio integrati e lasciate attivo e predefinito solo lo speaker usb.

Foto1: nuova versione in fase di sviluppo

![Screenshot](screenshot1.png)

Foto2: monitor con allarme

![Screenshot](screenshot3.png)

Foto3: monitor con allarme silenziato

![Screenshot](screenshot4.png)

Foto4: monitor con valori oltre il tempo massimo impostato

![Screenshot](screenshot5.png)

Foto5: prototipo reale (fronte)

![Screenshot](screenshot2.jpg)

Foto6: prototipo reale (retro)

![Screenshot](screenshot2bis.jpg)
