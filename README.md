## Kontaktberichte-Register

Deutsch | English
--- | ---
Enthält die Datendateien als auch ein Programm in Python für die Generierung eines Registers der Kontaktberichte von Billy Meier | Contains the data files and a generator program to produce a register for the contact reports written by Billy Meier

Aktuelle Version des Registers als PDF-Dokument:

TODO Freigaben (englisch *Releases*)

### Funktionsweise

Deutsch | English
--- | ---
Der Generator setzt aus den Datendateien und einer Vorlage ein Register zusammen, die dann gedruckt, angezeigt oder zB. zu einem PDF-Dokument weiterverarbeitet werden kann. | The generator assembles the register out of the data files and a template. The result can then be printed, displayed or further processed into a PDF document, for example.
Mögliche Ausgabeformate sind LaTeX (.tex) und HTML (.html). Um diese zu einem PDF-Dokument weiter zu verarbeiten, sind zB. PDF-Druckertreiber oder für .tex eine LaTeX-Umgebung wie zB. TeXlive notwendig; es kann auch ein Dienst im Internetz wie zB. ShareLatex verwendet werden. | Possible output formats are LaTeX (.tex) and HTML (.html). Further processing into PDF format requires additional software like a virtual PDF printer driver or similar converter software. For .tex output, a LaTeX distribution like TeXlive is required, or an online service like ShareLatex.
Die Ausgabe kann mit einigen Programmparametern angepasst werden. | The output can be customized with a few program arguments.

### Register selbst generieren

1. Falls noch nicht vorhanden, installiere eine Python-Distribution für dein System. Unter Linux ist Python üblicherweise schon vorinstalliert, für Mac OS und Windows gibt es auf der Python-Webseite eine

1. Starte den Generator ohne Parameter für eine interaktive Anpassung der Ausgabe oder mit Parametern für fortgeschrittene Benutzer. Eine Liste der Parameter erhältst du mit Hilfe von ```--hilfe```. TODO

1. Öffne oder verarbeite die Ausgabedateien weiter wie du möchtest.

  * Registriere dich auf ShareLatex und lade deine .tex-Datei hoch, um eine PDF-Version zu erhalten. Du musst dafür nichts installieren und die Verweise innerhalb des PDFs werden funktionieren.

  * Lade dir eine LaTeX-Distribution wie zB. [TeX Live](https://www.tug.org/texlive/) herunter, um eine PDF-Version zu erhalten.

  * Die HTML-Ausgabe kannst du in jedem Web-Browser öffnen und damit auch drucken, auch zu einem PDF-Drucker. Auch auf einem Tablett-Rechner oder Telefon kannst du sie betrachten.

  * Lade dir unter dem Stichwort "pdf printer" einen sogenannten virtuellen PDF-Drucker aus. Dies ist ein Drucker, der aber nicht real existiert, sondern jeden an ihn gesendeten Druckauftrag in eine PDF-Datei umwandelt. Unter Linux ist meistens schon ein PDF-Drucker vorinstalliert. Bei dieser Methode erhältst du in der PDF-Datei allerdings keine funktionierenden Verweise innerhalb des PDF-Dokuments.

  * Falls du eine Buchversion möchtest, sende deine PDF-Datei an eine Druckerei, die auch Einzelstücke druckt, wie zB. [Lulu](https://www.lulu.com/) oder [Epubli](http://www.epubli.de/). Dort kannst du deine PDF-Datei hochladen, einen Einband gestalten und wie in jedem anderen Internetz-Geschäft eine Bestellung durchführen.


### Mitmachen

Zur Synchronisierung der Mitwirkenden untereinander und zur einfachen und effizienten Integration von Änderungen wird _git_ verwendet. Eine sehr populäre Plattform, die auf dem offenen git aufbaut, ist _Github_. Es erlaubt über ein kostensloses Konto, Änderungen einzureichen und komfortabel einzupflegen.

Die direkte Variante online:

1. Lade dir das Programm git für dein System herunter. Unter Linux verwendest du dazu am Besten deine Paketverwaltung, unter Mac OS und Windows gibt es einen Klienten [von Github](https://desktop.github.com/).

1. Registriere dich [bei Github](https://www.github.com/).

1. Klicke nun rechts oben auf "Fork". Im nächsten Schritt wird eine Kopie des Kontaktberichte-Registers unter deinem Benutzernamen erstellt, zB. ```github.com/MeinBenutzer/kontaktberichte-register```.

1. Lade dir die Dateien deiner Kopie des git-Moduls (englisch: repository) herunter. Dazu gibst du im Klienten die Adresse deiner Kopie (englisch: Fork) an.

1. Mache deine Bearbeitungen an den Datendateien mit Hilfe eines Texteditors oder einer Tabellenkalkulation:

  * unter Windows: Notepad++

  * mit einem Texteditor unter Mac OS: [eine Auswahl](https://mac.appstorm.net/roundups/office-roundups/top-10-mac-text-editors/))

  * Linux: zB. Kate oder gedit

  * alle Systeme: OpenOffice oder LibreOffice

1. Speichere deine Änderungen ins git-Modul (englisch: commit).

1. Lade deine Änderungen hoch (englisch: Push).

1. Erstelle nun eine Aufforderung auf Einbindung (englisch: Pull Request). Dies kannst du entweder über den Github-Klienten oder über die Github-Webseite von deiner Kopie des Kontaktberichte-Registers aus veranlassen.

1. Die zuständigen Autoren erhalten nun eine Benachrichtigung, dass du Bearbeitungen gemacht hast, und diese

1. Nach Durchsicht, Qualitätssicherung und formeller Prüfung werden deine Änderungen nun eingepflegt und übernommen. Nach erfolgter Übernahme werden dann auch deine Ergänzungen aufscheinen.

1. Führe vor jeder weiteren Bearbeitung immer eine Aktualisierung bzw. Synchronisierung deiner lokalen Kopie auf deiner Festplatte mit Hilfe des Github-Klienten durch.


Variante ohne Github-Konto:

1. Diese Variante ist zwar für dich einfacher, bedeutet aber mehr Aufwand für den/die Betreuer des Registers, weil deine Änderungen manuell übernommen werden müssen.

1. Klicke dazu rechts oben auf dieser Seite auf "Clone or download". Du hast dort die Auswahl, einen bestenden git-Klienten zu verwenden oder "Open in Desktop" mit Hilfe des benutzerfreundlichen Github-Klienten. Klicke auf "Open in Desktop", installiere dir den Github-Klienten und lade dir damit die Dateien des Registers herunter.

1. Mache wie oben beschrieben deine Bearbeitungen.

1. Öffne den Github-Klienten und lasse dir die Änderungen anzeigen. Danach klicke auf "Generate Patch". Speichere dann die Änderungsdatei auf deiner Festplatte und schicke sie per E-Mail an den zuständigen Betreuer, ernst punkt rohlicek wiederpunkt at.

1. Nach Durchsicht, Qualitätssicherung und formeller Prüfung werden deine Änderungen nun manuell eingepflegt und übernommen.

1. Führe vor jeder weiteren Bearbeitung immer eine Aktualisierung bzw. Synchronisierung deiner lokalen Kopie auf deiner Festplatte mit Hilfe des Github-Klienten durch. Nach erfolgter Übernahme sollte nun auch deine abgeschickte Ergänzung aufscheinen.


Variante ohne git generell:

1. Diese Variante ist sowohl für dich als auch für den/die Betreuer des Registers ein Mehraufwand, weil deine Änderungen manuell verglichen und übernommen werden müssen und auch für dich, weil du immer deine lokale Kopie händisch aktuell halten musst, damit du auf dem aktuellen Stand bist.

1. Klicke dazu rechts oben auf dieser Seite auf "Clone or download". Klicke dann auf "Download ZIP". Dir wird ein ZIP-Archiv zum Herunterladen angeboten, das die Dateien des Registers enthält. Öffne und entpacke dieses auf einen Speicherort auf deiner Festplatte.

1. Mache wie oben beschrieben deine Bearbeitungen.

1. Schicke die von dir bearbeiteten Dateien per E-Mail an den zuständigen Betreuer, ernst punkt rohlicek wiederpunkt at.

1. Nach Durchsicht, Qualitätssicherung und formeller Prüfung werden deine Änderungen nun manuell eingepflegt und übernommen. Nach erfolgter Übernahme wird auch deine Ergänzung hier auf dieser Seite angezeigt übernommen.

1. Vor jeder weiteren Bearbeitung musst du Punkt 1 wiederholen, damit du immer auf Basis der aktuellen Version arbeitest. Verabsäumst du diesen Punkt, wird es für die Betreuer schwieriger, deine Ergänzungen effizient einzuarbeiten, weil sich in der Zwischenzeit durch andere Mitwirkende Änderungen ergeben haben können.


Fragen per E-Mail. TODO

Wenn du öfter Ergänzungen einreichst und diese gut ablaufen, dann kannst du auch Betreuer werden und erhältst direkten Schreibzugriff und ersparst die die Prozedur über einen Pull Request TODO.

Erstellen einer Freigabe:

1. Ausführen von ```daten/genversion.sh```, um die Hilfsdatei ```daten/VERSION``` zu erstellen, die von ```generate.py``` benutzt wird, um die Ersetzungsfelder ```DATEN-VERSION``` und ```DATEN-DATUM``` in die Ausgabedatei einzufügen.

1. Bei einer Freigabe auch immer die erstellte PDF-Datei als Anhang beifügen.


### Hinweise zur Bearbeitung

TODO

* Textkodierung: UTF-8
* Trennzeichen: Tabulator
* https://de.wikipedia.org/wiki/CSV_(Dateiformat)
* https://en.wikipedia.org/wiki/Comma-separated_values -> W3C SPARQL-Definition korrigiert CSV und TSV nochmal
* ... TODO noch viele weitere Angaben - alle Hakerln und Einstellmöglichkeiten beim Öffnen @ OO und Excel angeben

* keine neuen Zeilen, sondern nur ein langes Textfeld.

* TODO Vorsicht mit Microsoft Excel, nicht ".csv" als Format angeben, sondern "Text (Unicode) mit Trennzeichen (.txt)". TODO UTF-8, kein Windows-1252 oder Latin 1 oder ISO8859.

* Texteditor: Wenn deine Stichwörter ein Anführungszeichen (```"```) enthalten, dann muss dieses gemäß CSV-Format hervorgehoben werden und zwar durch zwei Anführungszeichen (```""```), ansonsten wird es als Ende des Tabellenfeldes interpretiert und das Datenformat ist ungültig.

* Achte darauf, keine schiefen Anführungszeichen zu verwenden, sondern nur die geraden Versionen (```"``` und ```'```)

* Wichtige Stichwörter, wie zB. Cassiopeia, Geschichte, große Reise, Lyraner, Lyra, Jitschi, Ashtar Sheran, Russland usw. hervorheben für die Stichwortliste und zwar mit ```##``` links und rechts einschließen. Auch Stichwörter mit mehreren Wörtern können sinnvoll sein, zB. ```Kontaktler!Jitschi``` und ```##Militärintervention der USA##```. Dies führt zu genaueren Stichwörtern als nur separat ```##Krieg##``` und ```##USA###```.

* Das Datumsformat und das Uhrzeitformat muss erhalten bleiben. Tabellenkalkulationen ändern gerne das Format auf ein lokales Format um. Das Format für Datumsangaben ist ISO 8601 "JJJJ-MM-TT", für Uhrzeiten das 24-Stunden-Format ohne Sekunde "11:00". Eventuell muss das Format per Befehl "Zellen formatieren..." wieder auf diese Formate gestellt werden.

### Technische Angaben zu den Datenstrukturen

Tabelle Buch:

* ```TITEL-KURZ``` (*Primärschlüssel*)
* ```TITEL```
* ```AUSGABE-JAHR```
* ```KB-VON``` (Name, nicht nur die Nummer)
* ```KB-BIS``` (Name, nicht nur die Nummer)
* ```EINLEITUNG```

Tabelle KB:

* ```NAME``` (*Primärschlüssel*) = Nummer + Sondersuffix zB. ```0a-sfath```
* ```NUMMER```
* ```SONDER-SUFFIX``` ein kleiner Ordnungsbuchstabe beginnend bei ```a``` zur Reihenfolgen-Information der Sonder-Teile von einigen Kontaktberichten.
* ```SONDER-TITEL``` falls vorhanden, ein Titel von quasi-Kontakten zB. in PPK1: Sfaths Erklärungen, ein telepathischer Kontakt mit Semjase, die Auftragsteile, die Asket-Kontakte usw.
* ```DATUM```
* ```ZEIT```
* ```ORT```
* ```PERSONEN```
* ```SAETZE-VON```
* ```SAETZE-BIS```
* ```EINLEITUNG```

Tabelle Satz:

* ```ID``` (*Primärschlüssel*) eine fortlaufende Nummer, derzeit unbenutzt
<!--* ```NAME``` (*Primärschlüssel*) im Format ```KBx ABCy``` zB. ```KB31 Sem123```-->
* ```NAME``` im Format ```AbcX``` zB. ```Sem123```
* ```KB``` (KB-Name, nicht nur die Nummer)
* ```REIHENFOLGE```
* ```SPRECHER```
* ```NUMMER```
* ```PPK-SEITE```
* ```SEM-SEITE```

Tabelle Thema:

* ```ID``` (*Primärschlüssel*) eine fortlaufende Nummer, derzeit unbenutzt
* ```KB``` (Name, nicht nur die Nummer)
* ```SATZ-VON``` (Name, nicht nur die Nummer)
* ```SATZ-BIS``` (Name, nicht nur die Nummer)
* ```INHALT``` (kurze Inhaltsangabe inkl. hervorgehobene Stichwörter für das alphabetische Stichwortregister) - zusammengefasst zwecks einfacherer Eingabe (kein Hin- und Herwechseln zwischen separaten INHALT- und STICHWOERTER-Feldern)


### Begründungen


#### Wahl der Programmiersprache

Deutsch | English
--- | ---
Python TODO

#### Wahl von git und Github als Basis

TODO

Ist aber natürlich in Ordnung, wenn jemand sich beteiligt und eine komfortablere Web-Oberfläche aufsetzt, wo man Kontaktberichte eintragen kann. Doch der Autor dieses Generators hat nicht die Zeit, dies aufzusetzen und sieht auch keine großen Vorteile darin, weil der Github-Klient recht benutzerfreundlich ist und darüber komfortabel Ergänzungen eingereicht werden können.

Wer Kalender und Kontakte mit seinem Telefon abgleichen kann oder Dropbox oder ein anderen Synchronisierungs-Werkzeug verwenden kann, für den wird auch Github kein Hindernis darstellen.

#### Wahl der Lizenzen

TODO

#### Wahl der Datenstrukturen

**Ziel** der Datenstrukturen ist es, die Position eines Themas bzw. Stichwörtern wieder auffindbar zu machen. Ein gesuchtes Thema soll mit Hilfe des Registers binnen einer Minute aufgefunden sein.

In einer Datei am Rechner kann man einfach rechnergestützt das gesamte Register durchsuchen, aber in einer gedruckten Version ist es unpraktikabel, das gesamte Register zu durchsuchen. Daher ist im Fall einer gedruckten Version ein alphabetisches Stichwortregister wichtig.

Grundsätzlich ist die Frage, wie genau die **Position** repräsentiert werden soll. Reicht es, zu wissen, dass irgendwo in diesem Kontaktbericht das gesuchte Thema behandelt wird? Einige Kontaktberichte sind 50 Seiten lang und ein Thema wird manchmal auch mehrmals in einem Kontakt angeschnitten. Der Zweck der Zeitersparnis wäre nur mit der KB-Nummer alleine also nicht optimal umgesetzt.

Eine genauere Form der Positions-Repräsentation könnte naiv die Seitenangabe sein. Doch das ist eine **Medium-bezogene Angabe** und ist keine verlässliche, sondern eine veränderliche Positionsangabe. Verständlicherweise können in Zukunft interessante Fotos, Zeitungsausschnitte von eingetroffenen Voraussagen oder bestätigten wissenschaftlichen Tatsachen oder andere Ausarbeitungen gemacht werden; es reicht schon wenn die Schriftgröße, der Zeilenabstand oder die Schriftart in einer neueren Ausgabe minimal geändert würde. Das hätte veränderte Abstände und einen veränderten Zeilenumbruch zur Folge und die gesamten Seitenangaben wären verschoben und unbrauchbar gemacht. Mit dieser Möglichkeit ist zu rechnen, daher ist statt einer Medium-bezogenen Positionsangabe eine **inhaltsbezogene** Angabe zu bevorzugen. Damit wären auch die Besitzer der Semjase-Blocks mit einbezogen.

Die einzige Möglichkeit der genauen inhaltsbezogenen Positionsangabe ist die **Satz-/Versnummer**. Ein erschwerender Faktor ist allerdings, dass die Vers-/Satznummern in den Kontaktberichten nicht linear fortlaufend, sondern Personen-bezogen sind. Jede Kontaktperson von Billy hat also ihre eigene, von 1 beginnende Satz-/Versnummerierung. Dies wird schon in KB28 und KB31 erkennbar. Gibt es in einem Kontakt mehrere Kontaktpersonen, dann steht folgendes abgedruckt:

  * Billy
  * Semjase 1.
  * Billy
  * Semjase 2.
  * Billy
  * Ptaah 1.
  * Semjase 3.
  * Billy
  * Semjase 4.
  * Billy
  * Ptaah 2.
  * usw.

Es ist (zumindest dem Autor dieser Zeilen) zwar unergründlich, warum Personen-bezogene/nicht-lineare Nummerierungen gemacht wurden und auch warum Billys Sätze nicht nummeriert wurden, enthalten doch auch sie manch wertvolle Information. Aber so liegen die Blöcke nun einmal vor, also muss damit gearbeitet werden.

Folglich muss für eine Positionsangabe auch der Name des Sprechers bzw. der Kontaktperson genannt werden, also zB. ```Sem12``` für Semjase 12. Satz/Vers. Diese ist innerhalb eines Kontaktberichts eindeutig. Eine eindeutige Positionsangabe wäre dann ```KB31 Sem31```.

Für eine Kontrolle hinsichtlich Vollständigkeit, Duplikate, Überlappungen usw. und auch um die Reihenfolge zu repräsentieren, ist es notwendig, einen **Index** der Sätze zu haben. Dort kann man auch die aktuelle Seitenzahl in der aktuellen Ausgabe des jeweiligen PPK- oder auch Semjase-Blocks als zusätzliche Information beifügen.

Insgesamt ergeben sich folgende 4 Dinge, die gespeichert werden müssen, im Bereich der relationalen Datenbanken **Enitäten** oder umgangssprachlich auch **Tabellen** genannt:

* Buch: Liste der Bücher, in denen ein Satz vorkommt. In diesem Fall die Plejadisch-plejarischen Kontaktberichte-Blöcke oder auch der Semjase-Blocks.
* KB: Liste der Kontaktberichte mit Information wie Datum, Uhrzeit, Personen usw.
* Satz: Liste und Reihenfolgen-Information der Sätze, wie sie in den Kontaktberichten stehen. Auch Information, welcher Sprecher und Satznummer als auch Seitenangabe in den PPK und Semjase-Blocks.
* Thema: Liste der Themen, die gesucht sind inklusive Stichwörtern mit Satz-von- und Satz-bis-Angaben.

Für die Register-Erstellung sind nur die Tabellen ```Buch```, ```KB``` (entspricht einem Kapitel im Register) und ```Thema``` (entspricht einem Eintrag im Register) erforderlich. Für diverse Kontrollen ist vor allem die Tabelle ```Satz``` wichtig.

#### CSV als Datenformat

TODO

Tabulatoren, weil dann nichts in Anführungszeichen gesetzt werden muss, ausser mehrzeilige Zellen-Inhalte, die aber nicht benutzt werden. Leichtere Bearbeitung in Texteditoren, keine Missverständnisse zwischen ```,``` und ```;``` als Spalten-Trennzeichen, was besonders bei Microsoft Excel Probleme macht (ändert automatisch das Trennzeichen je nach Lokalität, wegen unterschiedlichem Dezimaltrennzeichen im Englischen vs. im Deutschen).

Kann mit jeder Tabellenkalkulation bearbeitet werden, ob nun Open-/LibreOffice oder Excel oder ein anderes, jedes größere Betriebssystem, auch mit Texteditor (auch daher die Tabulatoren) bearbeitbar.

#### Gestaltung von git-Modulen

Deutsch | English
--- | ---
Man könnte ein separates git-Modul für die Datenhaltung verwenden, doch muss [gemäß dieser Anwort](https://stackoverflow.com/questions/36175383/can-a-github-repo-be-made-to-always-refer-to-the-latest-version-of-its-submodule) bei jeder neuen Version im Daten-Modul das Haupt-Modul mit aktualisiert werden, um auf die neue Daten-Version zu zeigen. Diese Vorgehensweise hat oft Vorteile (gesicherte Kompatibilität zu einer bestimmten Version), ist in diesem Fall aber nicht sinnvoll, daher werden die Daten hier im selben Modul gehalten. Vielleicht wird aber eine zukünftige Version von git den gewünschten Anwendungsfall ermöglichen. | It would be possible to keep the data files is a separate git-submodule, but this would require to update the main git module everytime to point to the new latest revision of the data sub-module. This policy has certain advantages (known compatibility to a specific version), but in this case, where the content is presumably updated more often than the generator program, this would create useless effort. Maybe there will be an added git feature for such use-cases in the future.

#### Sprache

TODO Deutsch als weltweite Sprache / "wertvolle weltweite Sprache"? Da war einmal was in den Kontaktberichten.

#### Format für Vorlagen

TODO Warum nicht ein Vorlagensystem wie zB. [Jinja](http://jinja.pocoo.org/)?

Es gibt einige sehr gute Vorlagensysteme, zugegeben. Und sie machen die Entwicklung von Generatoren auch sehr einfach. Doch erfolgt dadurch eine Bindung an eine Vorlagensprache und ev. sogar an eine Programmiersprache, in der die Vorlagensprache oder -bibliothek geschrieben ist.

Sie integrieren sich auch nicht in die erzeugten Datenformate (LaTeX, HTML). Es sollte möglich bleiben, die Vorlagen wohlgeformt in ihren Quellformaten zu halten, also dass sie gültiges LaTeX, gültiges HTML bleiben.

Aus diesen Gründen würde, zumindest vorerst, etwas gewählt, das in den Vorlage-Datenformaten gültig ist und trotzdem als Markierung erkennbar ist ohne mit dem normalen Text in der Vorlage zu kollidieren. Daher fiel die Wahl auf Punktuation, die aber selten in Kombination vorkommt, wie eben zwei Rufzeichen.

Der Inhalt der Felder ist grösstenteils aus den Datendateien, einige werden berechnet (zB. die Sprecherliste je KB).

Die Datendateien selbst sind so ausgelegt, dass sich auch andere Bücherreihen damit indizieren lassen, zB. die Geisteslehrbriefe, für die ein Stichwortverzeichnis sehr hilfreich wäre.
