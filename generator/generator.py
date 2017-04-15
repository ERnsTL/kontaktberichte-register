#!/usr/bin/env python3

"""Setzt ein Register der Kontaktberichte von Billy Meier in Form einer
weiterverarbeitbaren Quelldatei (LaTeX oder HTML) zusammen."""

import argparse
from enum import Enum
import sys
import datetime
import csv
from os import path
import re

class TemplateState(Enum):
    TemplatePrefix = 1  # looking for book begin
    BookPrefix = 2  # looking for chapter begin
    EntryPrefix = 3 # looking for entry begin
    Entry = 4   # looking for entry end
    ChapterPostfix = 5   # looking for chapter end
    BookPostfix = 6 # looking for book end
    TemplatePostfix = 7 # looking for template end

if __name__ == '__main__':
    # NOTE: argparse stdlibrary docs @ https://docs.python.org/3/library/argparse.html#choices
    # NOTE: argparse howto @ https://docs.python.org/3/howto/argparse.html
    #TODO the following arguments should have actual effect
    parser = argparse.ArgumentParser(description="Generiert ein Register der Kontaktberichte zur weiteren Verarbeitung.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    parser.add_argument("-m", "--missing", action="store_true")
    parser.add_argument("-n", "--kb-number", action="store_true")
    orientation = parser.add_mutually_exclusive_group()
    orientation.add_argument("-p", "--page-oriented", action="store_true")
    orientation.add_argument("-s", "--sentence-oriented", action="store_true")
    parser.add_argument("-P", "--page-number", action="store_true")
    parser.add_argument("-f", "--format", choices=['html', 'latex'], default="latex")
    parser.add_argument("-t", "--template", choices=["latex1", "html1"], default="latex1")  # TODO convert to file path
    #parser.add_argument("template", type=str, help="template name", default="latex1")
    #parser.add_argument("output", type=str, help="output file path", default="register.tex")
    parser.add_argument("-a", "--authors", choices=['lines', 'commas'], default="lines")    #TODO Autoren mit \\ oder , getrennt -> Argument
    parser.add_argument("-o", "--output", type=str, help="output file path", default="register.tex")
    parser.add_argument("-V", "--version", action="store_true")
    args = parser.parse_args()
    #TODO interactive mode

    if args.version:
        print("Version: 1.0.0-alpha0.2.0 (2016-07-07)")
        sys.exit(0)

    # parse template line by line, resulting in separate line lists for each part
    filename = ("main.tex" if args.format == "latex" else "index.html")
    if args.format == "html":
        print("FEHLER: HTML-Ausgabe noch unimplementiert -> Bitte als Format 'latex' angeben.")
        sys.exit(1)
    templateFile = open("./vorlagen/{}/{}".format(args.template, filename), 'r')
    outFile = open(args.output, 'w')
    state = TemplateState.TemplatePrefix
    # NOTE: Hierarchy and ordering of template parts:
    # template prefix
    #   book prefix
    #       chapter prefix
    #           entry
    #       chapter postfix
    #   book postfix
    # template postfix
    templatePrefix = []
    templatePostfix = []
    bookPrefix = []
    bookPostfix = []
    chapterPrefix = []
    chapterPostfix = []
    entryTemplate = []
    delimiter = '!!'
    for line in templateFile:
        if state == TemplateState.TemplatePrefix:
            if delimiter + "BUCH-ANFANG" + delimiter in line:
                # NOTE: discarding line
                state = TemplateState.BookPrefix
            else:
                # still in template prefix, save line
                templatePrefix.append(line)
        elif state == TemplateState.BookPrefix:
            if delimiter + "KAPITEL-ANFANG" + delimiter in line:
                # NOTE: discarding line
                state = TemplateState.EntryPrefix
            else:
                # still in book prefix, save line
                bookPrefix.append(line)
        elif state == TemplateState.EntryPrefix:
            if delimiter + "EINTRAG-ANFANG" + delimiter in line:
                # NOTE: discard line
                state = TemplateState.Entry
            else:
                # still in entry, save line
                chapterPrefix.append(line)
        elif state == TemplateState.Entry:
            if delimiter + "EINTRAG-ENDE" + delimiter in line:
                # NOTE: discard line
                state = TemplateState.ChapterPostfix
            else:
                # still after entry in chapter, save line
                entryTemplate.append(line)
        elif state == TemplateState.ChapterPostfix:
            if delimiter + "KAPITEL-ENDE" + delimiter in line:
                # NOTE: discard line
                state = TemplateState.BookPostfix
            else:
                # still after chapter in book, save line
                chapterPostfix.append(line)
        elif state == TemplateState.BookPostfix:
            if delimiter + "BUCH-ENDE" + delimiter in line:
                ## NOTE: discard line
                state = TemplateState.TemplatePostfix
            else:
                # still after chapter in template, save line
                bookPostfix.append(line)
        elif state == TemplateState.TemplatePostfix:
            # still after book in template, save line
            # NOTE: waiting for end of file, no further state
            templatePostfix.append(line)
        else:
            print("FEHLER: Unbekannter Einlese-Zustand {} -> Programmfehler liegt vor.".format(state))
            sys.exit(2)
    templateFile.close()
    if state != TemplateState.TemplatePostfix:
        which = "ERROR"
        if state == TemplateState.TemplatePrefix:
            which = delimiter + "BUCH-ANFANG" + delimiter
        elif state == TemplateState.BookPrefix:
            which = delimiter + "KAPITEL-ANFANG" + delimiter
        elif state == TemplateState.EntryPrefix:
            which = delimiter + "EINTRAG-ANFANG" + delimiter
        elif state == TemplateState.Entry:
            which = delimiter + "EINTRAG-ENDE" + delimiter
        elif state == TemplateState.ChapterPostfix:
            which = delimiter + "KAPITEL-ENDE" + delimiter
        elif state == TemplateState.BookPostfix:
            which = delimiter + "BUCH-ENDE" + delimiter
        elif state == TemplateState.TemplatePostfix:
            which = "EOF"   # NOTE: should never happen
        print("FEHLER: Markierung {} fehlt in der Vorlage -> Markierungen auf Vollständigkeit überprüfen.".format(which))
        sys.exit(3)

    # read data files
    dialect = "excel-tab"
    books = []  # NOTE: using list because it is ordered as is iterating over it
    chapters = {}
    entries = {}
    sentences = {}
    #TODO harmonize _ and - between csv <-> template
    dataDir = "../daten/"
    # Bücher/books
    with open(dataDir + "buch.csv", 'r') as booksFile:
        bookList = csv.DictReader(booksFile, dialect=dialect)
        for book in bookList:
            bookTitle = book["TITEL-KURZ"]
            books.append(book)
    # KB/chapters
    with open(dataDir + "kb.csv", 'r') as chaptersFile:
        chapterList = csv.DictReader(chaptersFile, dialect=dialect)
        curBookIndex = 0
        curBookLastKB = None
        curBookKey = None
        foundBookLastKB = False
        for chapter in chapterList:
            # get new book info if info is empty/null/None
            if curBookLastKB == None:
                curBookLastKB = books[curBookIndex]["KB-BIS"]
                curBookKey = books[curBookIndex]["TITEL-KURZ"]
                chapters[curBookKey] = []
                foundBookLastKB = False
            # copy current KB to current book
            if args.verbose:
                print("INFO: Buch {} hat neuen KB/Kapitel {}.".format(curBookKey, chapter["NAME"]))
            chapters[curBookKey].append(chapter)
            # get new book info if this is the last KB/chapter of the current book and if there is at least one more book
            if chapter["NAME"] == curBookLastKB and curBookIndex < len(books)-1:
                curBookIndex += 1
                curBookLastKB = books[curBookIndex]["KB-BIS"]
                curBookKey = books[curBookIndex]["TITEL-KURZ"]
                chapters[curBookKey] = []   #TODO this creates empty entry for next book, even if that has no entries at all, might be misleading
                foundBookLastKB = True
        if foundBookLastKB == False and args.quiet == False:
            print("WARNUNG: Kontaktberichte fehlen: Zumindest letzter KB {} von Buch {} fehlt in KB-Tabelle.".format(curBookLastKB, curBookKey))
    # Themen/subjects/entries
    with open(dataDir + "thema.csv", 'r') as entriesFile:
        entriesList = csv.DictReader(entriesFile, dialect=dialect)
        for entry in entriesList:
            chapterName = entry["KB"]
            if chapterName not in entries:
                # create entry for that chapter/KB
                entries[chapterName] = []
            # copy entry
            entries[chapterName].append(entry)
    # Sätze/Verse/sentences index
    with open(dataDir + "satz.csv", 'r') as sentencesFile:
        sentencesList = csv.DictReader(sentencesFile, dialect=dialect)
        for sentence in sentencesList:
            chapterName = sentence["KB"]
            if chapterName not in sentences:
                # create entry for that chapter/KB
                sentences[chapterName] = []
            # copy entry
            sentences[chapterName].append(sentence)

    # generate output file
    #TODO check for unused/unneeded fields in template file and data files
    #    if delimiter + "" + delimiter in line:
    #        result =
    #        line = line.replace(delimiter + "" + delimiter, result)

    # template prefix; may contain ERZEUGT-DATUM, DATEN-VERSION, DATEN-DATUM, DATEN-DATUMZEIT    #TODO ../.git/ORIG_HEAD
    for line in templatePrefix:
        if delimiter + "ERZEUGT-DATUM" + delimiter in line:
            result = datetime.date.today().isoformat()
            line = line.replace(delimiter + "ERZEUGT-DATUM" + delimiter, result)
        if delimiter + "DATEN-VERSION" + delimiter in line:
            versionFile = "../daten/VERSION"
            gitHeadFile = "../.git/ORIG_HEAD"
            if path.isfile(versionFile):
                with open(versionFile, 'r') as f:
                    dataVersion = f.readline().rstrip().partition(" ")[0]
                    line = line.replace(delimiter + "DATEN-VERSION" + delimiter, dataVersion)
                    # NOTE: closes file automatically at end of block
            elif path.isfile(gitHeadFile):
                with open("../.git/ORIG_HEAD", 'r') as f:
                    #TODO try..catch block resp. catch file open error
                    first_line = f.readline().rstrip()[:6]
                    line = line.replace(delimiter + "DATEN-VERSION" + delimiter, first_line)
                    # NOTE: closes file automatically at end of block
            else:
                print("FEHLER: Konnte Daten-Version für Ersetzungsfeld DATEN-VERSION nicht finden -> genversion.sh starten oder git-Metadaten laden.")
        if delimiter + "DATEN-DATUMZEIT" + delimiter in line :
            versionFile = "../daten/VERSION"
            if path.isfile(versionFile):
                with open(versionFile, 'r') as f:
                    dataDateTime = f.readline().rstrip().partition(" ")[2]
                    line = line.replace(delimiter + "DATEN-DATUMZEIT" + delimiter, dataDateTime)
                    # NOTE: closes file automatically at end of block
            #TODO implement alternative approach using just git files directly without genversion.sh
            else:
                print("FEHLER: Konnte Daten-Version für Ersetzungsfeld DATEN-DATUMZEIT nicht finden -> genversion.sh starten")
        if delimiter + "DATEN-DATUM" + delimiter in line :
            versionFile = "../daten/VERSION"
            if path.isfile(versionFile):
                with open(versionFile, 'r') as f:
                    dataDate = f.readline().rstrip().partition(" ")[2].partition(" ")[0]
                    line = line.replace(delimiter + "DATEN-DATUM" + delimiter, dataDate)
                    # NOTE: closes file automatically at end of block
            #TODO implement alternative approach using just git files directly without genversion.sh
            else:
                print("FEHLER: Konnte Daten-Version für Ersetzungsfeld DATEN-DATUM nicht finden -> genversion.sh starten")
        # else/default case
        if delimiter in line and args.quiet == False:
            print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
        outFile.writelines([line])

    # for each book...
    for book in books:
        # book prefix; may contain TITEL, AUSGABE-JAHR, KB-VON, KB-BIS, KB-VON-DATUM, KB-BIS-DATUM
        for line in bookPrefix:
            if delimiter + "TITEL" + delimiter in line:
                #print("typ: {}".format(type(book).__name__))
                result = book["TITEL"]
                line = line.replace(delimiter + "TITEL" + delimiter, result)
            if delimiter + "AUSGABE-JAHR" + delimiter in line:
                result = book["AUSGABE-JAHR"]
                line = line.replace(delimiter + "AUSGABE-JAHR" + delimiter, result)
            if delimiter + "KB-VON-NAME" + delimiter in line:
                result = book["KB-VON"]
                line = line.replace(delimiter + "KB-VON-NAME" + delimiter, result)
            if delimiter + "KB-BIS-NAME" + delimiter in line:
                result = book["KB-BIS"]
                line = line.replace(delimiter + "KB-BIS-NAME" + delimiter, result)
            if delimiter + "KB-VON-DATUM" + delimiter in line:
                # get first chapter from book
                bookFirstChapter = book["KB-VON"]
                # find that chapter in chapters, get its date
                #TODO sanity checks:
                #TODO does NAME field exist before comparison?
                #TODO check if found, otherwise warning
                dateFirst = "(erster KB im Buch nicht vorhanden)"
                bookKey = book["TITEL-KURZ"]
                if bookKey in chapters:
                    for chapter in chapters[bookKey]:
                        if chapter["NAME"] == bookFirstChapter:
                            dateFirst = chapter["DATUM"]
                            break
                    result = "{}".format(dateFirst)  #TODO customisable date format
                else:
                    #TODO warning
                    result = "(kein KB im Buch vorhanden)"
                line = line.replace(delimiter + "KB-VON-DATUM" + delimiter, result)
            if delimiter + "KB-BIS-DATUM" + delimiter in line:
                # get last chapter from book
                bookLastChapter = book["KB-BIS"]
                # find that chapter in chapters, get its date
                #TODO sanity checks:
                #TODO does NAME field exist before comparison?
                #TODO check if found, otherwise warning
                dateLast = "(letzter KB im Buch nicht vorhanden)"
                bookKey = book["TITEL-KURZ"]
                if bookKey in chapters:
                    for chapter in chapters[bookKey]:
                        if chapter["NAME"] == bookLastChapter:
                            dateLast = chapter["DATUM"]
                            break
                    result = "{}".format(dateLast)  #TODO customisable date format
                else:
                    #TODO warning
                    result = "(kein KB im Buch vorhanden)"
                line = line.replace(delimiter + "KB-BIS-DATUM" + delimiter, result)
            if delimiter in line and args.quiet == False:
                print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
            outFile.writelines([line])

        # chapter prefix; may contain NAME, DATUM, ZEIT, PERSONEN, EINLEITUNG
        #TODO also @ csv: SONDER-SUFFIX, SONDER-NAME
        curBook = book["TITEL-KURZ"]
        if curBook in chapters:
            for chapter in chapters[curBook]:
                for line in chapterPrefix:
                    if delimiter + "NAME" + delimiter in line:
                        result = chapter["NAME"]  #TODO harmonize name csv <-> template
                        line = line.replace(delimiter + "NAME" + delimiter, result)
                    if delimiter + "DATUM" + delimiter in line:
                        result = chapter["DATUM"]   #TODO harmonize name csv <-> template
                        line = line.replace(delimiter + "DATUM" + delimiter, result)
                    if delimiter + "ZEIT" + delimiter in line:
                    	# expected format ist hh:mm:ss
                        result = chapter["ZEIT"][:5]   #TODO harmonize name csv <-> template
                        line = line.replace(delimiter + "ZEIT" + delimiter, result)
                    if delimiter + "PERSONEN" + delimiter in line:
                        result = chapter["PERSONEN"]
                        line = line.replace(delimiter + "PERSONEN" + delimiter, result)
                    if delimiter + "EINLEITUNG" + delimiter in line:
                        result = chapter["EINLEITUNG"]
                        line = line.replace(delimiter + "EINLEITUNG" + delimiter, result)
                    if delimiter in line and args.quiet == False:
                        print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
                    outFile.writelines([line])

                # entries; may contain SATZ-VON, SATZ-BIS, SEITE-VON, SEITE-VON-BIS, INHALT
                #TODO @ csv there is also: KB (not needed in this case, because entry list is already filtered by KB/chapter)
                curChapter = chapter["NAME"]
                if curChapter in entries:
                    for entry in entries[curChapter]:
                        for line in entryTemplate:
                            #if delimiter + "" + delimiter in line:
                            #    result = chapter[""]
                            #    line = line.replace(delimiter + "" + delimiter, result)
                            if delimiter + "SATZ-VON" + delimiter in line:
                                result = entry["SATZ-VON"]
                                line = line.replace(delimiter + "SATZ-VON" + delimiter, result)
                            if delimiter + "SATZ-BIS" + delimiter in line:
                                result = entry["SATZ-BIS"]
                                line = line.replace(delimiter + "SATZ-BIS" + delimiter, result)
                            if delimiter + "SEITE-VON" + delimiter in line:
                                result = "TODO"    #TODO berechnetes Feld
                                line = line.replace(delimiter + "SEITE-VON-BIS" + delimiter, result)
                            if delimiter + "SEITE-VON-BIS" + delimiter in line:
                                #TODO sanity checks:
                                #TODO does sentences[curChapter] exist?
                                #TODO does NAME field exist before comparison?
                                #TODO check if found, otherwise warning
                                # find start sentence and get page number
                                pageStart = 0
                                for sentence in sentences[curChapter]:
                                    if sentence["NAME"] == entry["SATZ-VON"]:
                                        pageStart = sentence["PPK-SEITE"]
                                        break
                                # find end sentence and get page number
                                pageEnd = 0
                                for sentence in sentences[curChapter]:
                                    if sentence["NAME"] == entry["SATZ-VON"]:
                                        pageEnd = sentence["PPK-SEITE"]
                                        break
                                # generate result
                                if pageStart != pageEnd:
                                    result = "S{}/{}".format(pageStart, pageEnd)
                                else:
                                    #TODO make these two configurable
                                    #result = "S{}".format(pageStart)
                                    result = pageStart
                                line = line.replace(delimiter + "SEITE-VON-BIS" + delimiter, result)
                            if delimiter + "SPRECHER" + delimiter in line:
                                #TODO berechnetes Feld aus SATZ-Tabelle
                                result = "TODO"
                                line = line.replace(delimiter + "SPRECHER" + delimiter, result)
                            if delimiter + "INHALT" + delimiter in line:
                                result = entry["INHALT"]
                                # replace keyword markers
                                # NOTE: for LaTeX: !!keyword!! into \index{keyword}
                                numKeywordMarkers = result.count("!!")
                                if numKeywordMarkers > 0:
                                    # sanity check
                                    # NOTE: python regex howto @ https://docs.python.org/3/howto/regex.html
                                    # NOTE: regex tester @ http://www.regexr.com/
                                    # remove all correct keyword matches
                                    resultCheck = re.sub('(!![^!]+?(![^!]+?)?!!)', "", result)
                                    # if there are still any left, then those are the uncorrect ones - report error
                                    if resultCheck.count("!") > 0:
                                        print("FEHLER: Abwegige Rufzeichen in Inhalt von Eintrag KB {} V {} bis {}: Position: {}".format(entry["KB"], entry["SATZ-VON"], entry["SATZ-BIS"], resultCheck))
                                        sys.exit(3)

                                    # process keyword markers
                                    while "!!" in result:
                                        # separate out beginning
                                        # NOTE: prefix ... !! rest ........
                                        prefix = result.partition("!!")[0]
                                        #print("prefix: {}".format(prefix))
                                        right = result.partition("!!")[2]
                                        #print("right: {}".format(right))
                                        # find end in rest
                                        # NOTE: keyword !! ... postfix
                                        # NOTE: keyword can be further divided like this: [main-keyword]![sub-keyword]
                                        keyword = right.partition("!!")[0]  #TODO sub-keywords for HTML
                                        #print("keyword: {}".format(keyword))
                                        postfix = right.partition("!!")[2]
                                        #print("postfix: {}".format(postfix))
                                        # put it together
                                        #NOTE: To escape a single { or }, double it. The backlash is ecaped using regular backlash.
                                        keywordReplaced = ("\\index{{{}}}".format(keyword) if args.format == "latex" else "TODO")
                                        result = prefix + keywordReplaced + postfix
                                #TODO stichworthervorhebung
                                line = line.replace(delimiter + "INHALT" + delimiter, result)
                            if delimiter in line and args.quiet == False:
                                print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
                            outFile.writelines([line])
                else:
                    if args.quiet == False:
                        print("WARNUNG: Keine Einträge für KB {} in Thema-Tabelle vorhanden -> Bitte Daten ergänzen.".format(curChapter))

                # chapter postfix (no variables)
                outFile.writelines(chapterPostfix)
        else:
            if args.quiet == False:
                print("WARNUNG: Keine Einträge für Buch {} in KB-Tabelle vorhanden -> Bitte Daten ergänzen.".format(curBook))

        # book postfix (no variables)
        outFile.writelines(bookPostfix)

    # template postfix, may contain AUTOREN
    for line in templatePostfix:
        if delimiter + "AUTOREN" + delimiter in line:
            #autorenSeparator = (" \\\\" if args.format == "latex" else "<br>")
            with open("../daten/AUTHORS", 'r') as autorenFile:
                #TODO try..catch block resp. catch file open error
                autoren = autorenFile.readlines()
                autorenOut = ""
                for autor in autoren:
                    autor = autor.rstrip()
                    autorenOut += line.replace(delimiter + "AUTOREN" + delimiter, autor)
                    #autoren = [autor.rstrip() for autor in autoren]
                #line = line.replace(delimiter + "AUTOREN" + delimiter, (autorenSeparator + "\n").join(autoren))
                line = autorenOut
                # NOTE: closes file automatically at end of block
        if delimiter in line and args.quiet == False:
            print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
        outFile.writelines([line])

    # close output file
    outFile.close()
