e2openplugin-PushService
========================

A flexible event notification service for Enigma2. Never miss any free space warning, update or timer conflict.


Lasst euch von eurer Dreambox über aktuelle Vorgänge informieren.

PushService (kurz PS) wird in konfigurierbaren, regelmäßigen Abständen oder zu bestimmten Events ausgeführt.
Schlägt ein Plugin Alarm werdet Ihr über die konfigurierten Services benachrichtigt.

Hier ein Beispiel für eine Email-Benachrichtigung:
Zitat:
Subject: DM8000 PushService: Free space warning
Free disk space limit has been reached:
Path: /media/hdd/movie
Limit: 100 GB
Left: 88 GB
Provided by Dreambox Plugin PushService
C 2012 by betonme @ IHAD


Tastenbelegung im Setup:
Alle Tasten sind beschriftet und schaut in die Hilfe (es gibt keine versteckten Tasten mehr)
Die Grundkonfiguration von PS wird in der E2 Config abgespeichert.
Alle Service- und Plugin-Einstellungen werden in einer XML-Datei abgelegt (Default = /etc/enigma2/pushservice.xml).

PS Grundkonfiguration:
Enable PushService = True
Dreambox name (Mail Subject) = Dreambox
Config file = /etc/enigma2/pushservice.xml
Start time (HH:MM) = 1:00 Uhr
Period in hours (0=disabled) = 24
Run on boot = True

Aktuelle Services mit Beispielen und Optionen:
SMTP:
Mail Versand über SMTP
-SMTP Server = smtp.server.com
-SMTP Port = 587
-SMTP SSL = True
-TimeOut
-User name
-Password
-Mail from = abc@provider.com
-Mail to or leave empty
GNTP:
Growl Network Transport Protocol
Getestet mit Growl for Windows, sollte aber auch mit Snarl und Prowl funktionieren
-Growl Host name
-Growl Port
-Timeout
-Password
-Send as sticky
-Send with priority
PopUp:
Einfaches E2 PopUp.
Anmerkung: Ein E2 PopUp wird erst angezeigt, nachdem alle Screens/Dialoge geschlossen wurden.
-TimeOut

Aktuelle Plugins mit Beispielen und Optionen:
FreeSpace: 
Ihr gebt einen Pfad vor und den gewünschten freien Speicher, liegt der ermittelte freie Speicherplatz darunter, bekommt Ihr eine eMail.
Kann mehrfach hinzugefügt werden, damit verschiedene Speicher geprüft werden können.
-Allow HDD wake up = False
-Where to check free space = /media/hdd/movie
-Free space limit in GB = 100GB
DeactivatedTimers: 
Der AutoTimer trifft auf einen Timerkonflikt und kann eine Sendung nicht aufnehmen und erstellt deswegen einen deaktivierten Timer (muss aktiviert werden). PS würde euch in dem Fall eine eMail mit dem betreffenden Timer zuschicken.
Vergesst nicht folgende Option im AutoTimer Setup einzuschalten:
"Add timer as disabled on conflict" ("Bei Konflikt deaktivierten Timer hinzufügen")
- Remove deactivated timer(s) after successful transmission = False (On False PS will tag them as DeactivatedTimerPushed)
CrashLog: 
Angelehnt an die DMM Funktion. Ihr seid außer Haus und es tritt ein GS auf, die Dreambox startet automatisch neu und sendet euch eine Benachrichtigung mit dem CrashLog im Anhang.
-Delete crashlog(s) after successful transmission = False (On False PS will rename them to .pushed)
RecordSummary:
Eine Liste aller getätigten Aufnahmen wird euch zugeschickt.
-Remove finished timer(s) only after = False (On False PS will tag them as FinishedTimerPushed)
RecordNotification:
Ihr bekommt eine sofortige Benachrichtigung, wenn eine Aufnahme startet oder beendet wird.
-Send notification on record start = False
-Send notification on record end = True
IPKGUpdateNotification:
Wenn Updates bereitstehen bekommt Ihr eine Liste aller Plugins mit der aktuell installierter Version und der Version des Updates.
-Start update check if not done yet = False

Weitere Service-/Plugin-Module können sehr einfach zur Laufzeit ohne Neustart hinzugefügt werden.
Wenn das Setup geöffnet wird, werden die Einstellungen und Module neu eingelesen.
Jedes Modul kann weitere Einstellungen bereitstellen, die dann automatisch in der Config eingebunden werden.

Roadmap:
Konfiguration / Optionen übersetzen
Öffentlicher Beta-Test
Schwerkraft GIT -> Feed
Lokalisierung ist vorbereitet, somit kann jeder dazu beisteuern.

Installation:
IPKG installieren

Anleitung zum Erstellen eines Plugin-Moduls:
Es gibt ein Paar Rahmenbedingungen für die Module:
Die py-Datei und der class-Namen müssen übereinstimmen
Die class muss eine subclass der ServiceBase/PluginBase sein
Die Bedingungen werden Beim Laden der Module auch geprüft, Fehler werden auf der Konsole ausgegeben.

Alles weitere ist optional und hängt von Eurem Modul ab:
init: Sollte die Optionen behinhalten (self.setOptions ...)
(Das Speichern/Laden/Setup-Eintrag wird alles von der Basisklasse erledigt)
begin: Wird aufgerufen, wenn PS gestartet wird
end: Wird aufgerufen, wenn PS gestoppt wird

Services:
push: Sendet eure Benachrichtigung
cancel: Aufforderung zum Abbruch der Push-Funktion

Plugins:
run: Führt eure Prüfungen durch und übergebt gegebenfalls Subject, Body(optional), Attachments(optional) an die callback.
callback: Callback bei erfolgreichem Versand
errback: Callback wenn ein Fehler beim Versenden auftritt

Change-Log:
0.1
Erstes Release
0.1.1
IPK Release
0.1.2
Bugfix: Mailto Feld wurde nicht verarbeitet
0.1.3
Bugfix: SSL Versand überarbeitet
0.2
Services sind nun auch über Module konfigurierbar
SMTP Config ist somit auch im XML abgelegt
Neu: GNTP, PopUp
Modul-Optionen sind nun sortiert
Alle Module können nun asynchron laufen (Es werden Callbacks anstelle von returns verwendet)
0.2.1
Bugfix: Crash in RecordNotification behoben
Global PushService Handhabung verbessert
0.2.2
PS ist jetzt im Schwerkraft Git
Identisch zu der 0.2.1
0.2.3
Bugfix: Fehler beim Laden von PS
Plugins umbenannt zu Controller um Namenskonflikten mit den E2 Plugins vorzubeugen (Ändert eure XML!)
Exceptions beim Parsen der XML Config werden jetzt abgefangen
Bugfix: Deaktivierte Service wurden ausgeführt
0.2.4
OE2.0 tested
Config Skin separiert
0.2.5
Fixed Missing Skin
0.2.6
New Controller: Active timers
Small translation changes