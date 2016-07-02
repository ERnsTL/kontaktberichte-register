# kontaktberichte-register
Datendateien und Generatorprogramm für ein Register der Kontaktberichte von Billy Meier

## Begründungen

### Gestaltung von git-Modulen

Deutsch | English
--- | ---
Man könnte ein separates git-Modul für die Datenhaltung verwenden, doch muss [gemäß dieser Anwort](https://stackoverflow.com/questions/36175383/can-a-github-repo-be-made-to-always-refer-to-the-latest-version-of-its-submodule) bei jeder neuen Version im Daten-Modul das Haupt-Modul mit aktualisiert werden, um auf die neue Daten-Version zu zeigen. Diese Vorgehensweise hat oft Vorteile (gesicherte Kompatibilität zu einer bestimmten Version), ist in diesem Fall aber nicht sinnvoll, daher werden die Daten hier im selben Modul gehalten. Vielleicht wird aber eine zukünftige Version von git unseren Anwendungsfall ermöglichen. | It would be possible to keep the data files is a separate git-submodule, but this would require to update the main git module everytime to point to the new latest revision of the data sub-module. This policy has certain advantages (known compatibility to a specific version), but in this case, where the content is presumably updated more often than the generator program, this would create useless effort. Maybe there will be an added git feature for such use-cases in the future.
