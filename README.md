# nightscout-python-monitor
Un monitor in python che si basa su nightscout e GUIZero. 
Hardware necessario un raspberry pi (almeno il 3) e un monitor gpio/hdmi da 5 pollici con touchscreen.
Software necessario python versione 3 con GUIZero installato.

Nel file monitor.py bisogna mettere HOST-NIGHTSCOUT e TOKEN relativi al proprio nightscout.

L'impaginazione è adeguata per un monitor con risoluzione 800x480.

Il tasto silenzia, se attivo, fa suonare gli allarmi ogni 30 minuti. Sennò suona ogni 5 finchè i valori non tornano in range.

PS: per adesso gli allarmi NON suonano perchè sto cercando una soluzione smart per "dare voce" al raspberry (mini speaker penso).

Foto1: nuova versione in fase di sviluppo

![Screenshot](screenshot.png)

Foto2: vecchia versione

![Screenshot](screenshot2.png)

