#!/usr/bin/env python3

"""Setzt ein Register der Kontaktberichte von Billy Meier in Form einer
weiterverarbeitbaren Quelldatei (LaTeX oder HTML) zusammen."""

import argparse
from enum import Enum
import sys
import datetime
import csv
from os import path

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
        print("Version: 0.1.0 (2016-07-04)")
        sys.exit(0)

    # parse template line by line, resulting in separate line lists for each part
    filename = ("main.tex" if args.format == "latex" else "index.html")
    if args.format == "html":
        print("FEHLER: HTML-Ausgabe noch unimplementiert. -> Bitte als Format 'latex' angeben.")
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
    #TODO harmonize _ and - between csv <-> template
    with open('../daten/meta.csv', 'r') as bookListFile:
        bookList = csv.DictReader(bookListFile, dialect=dialect)
        for book in bookList:
            #print(book['BUCH_TITEL_KURZ'], book['BUCH_TITEL'], book['BUCH_AUSGABE_JAHR'], book['KAPITEL_VON'], book['KAPITEL_BIS'], book['EINLEITUNG'])
            # read corresponding book meta file for chapter list
            bookTitle = book['BUCH_TITEL_KURZ']
            books.append(book)
            bookMetaFileName = "../daten/{}_meta.csv".format(bookTitle.lower())
            entriesFileName = "../daten/{}.csv".format(bookTitle.lower())
            with open(bookMetaFileName, 'r') as bookMetaFile:
                chapterList = csv.DictReader(bookMetaFile, dialect=dialect)
                chapters[bookTitle] = list(chapterList)  # list copy
            with open(entriesFileName, 'r') as entriesFile:
                entriesList = csv.DictReader(entriesFile, dialect=dialect)
                entries[bookTitle] = list(entriesList)   # list copy

    # generate output file
    #TODO check for unused/unneeded fields in template file and data files
    #    if delimiter + "" + delimiter in line:
    #        result =
    #        line = line.replace(delimiter + "" + delimiter, result)

    # template prefix; may contain ERZEUGT-DATUM, DATEN-VERSION, DATEN-DATUM    #TODO ../.git/ORIG_HEAD
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
        if delimiter + "DATEN-DATUM" + delimiter in line :
            versionFile = "../daten/VERSION"
            if path.isfile(versionFile):
                with open(versionFile, 'r') as f:
                    dataDate = f.readline().rstrip().partition(" ")[2]
                    line = line.replace(delimiter + "DATEN-DATUM" + delimiter, dataDate)
                    # NOTE: closes file automatically at end of block
            #TODO implement alternative approach using just git files directly without genversion.sh
            else:
                print("FEHLER: Konnte Daten-Version für Ersetzungsfeld DATEN-DATUM nicht finden -> genversion.sh starten")
        # else/default case
        if delimiter in line :
            print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
        outFile.writelines([line])

    # for each book...
    for book in books:
        # book prefix; may contain BUCH-TITEL, BUCH-AUSGABE-JAHR, KAPITEL-VON, KAPITEL-BIS, KAPITEL-VON-DATUM, KAPITEL-BIS-DATUM
        for line in bookPrefix:
            if delimiter + "BUCH-TITEL" + delimiter in line:
                #print("typ: {}".format(type(book).__name__))
                result = book["BUCH_TITEL"]
                line = line.replace(delimiter + "BUCH-TITEL" + delimiter, result)
            if delimiter + "BUCH-AUSGABE-JAHR" + delimiter in line:
                result = book["BUCH_AUSGABE_JAHR"]
                line = line.replace(delimiter + "BUCH-AUSGABE-JAHR" + delimiter, result)
            if delimiter + "KAPITEL-VON" + delimiter in line:
                result = book["KAPITEL_VON"]
                line = line.replace(delimiter + "KAPITEL-VON" + delimiter, result)
            if delimiter + "KAPITEL-BIS" + delimiter in line:
                result = book["KAPITEL_BIS"]
                line = line.replace(delimiter + "KAPITEL-BIS" + delimiter, result)
            if delimiter + "KAPITEL-VON-DATUM" + delimiter in line:
                result = "TODO"    #TODO generate from chapters list
                line = line.replace(delimiter + "KAPITEL-VON-DATUM" + delimiter, result)
            if delimiter + "KAPITEL-BIS-DATUM" + delimiter in line:
                result = "TODO"   #TODO generate
                line = line.replace(delimiter + "KAPITEL-BIS-DATUM" + delimiter, result)
            if delimiter in line :
                print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
            outFile.writelines([line])

        bookTitle = book["BUCH_TITEL_KURZ"]
        for chapter in chapters[bookTitle]:
            # chapter prefix; may contain KAPITEL-NR, KAPITEL-DATUM, KAPITEL-UHRZEIT, PERSONEN, EINLEITUNG
            #TODO @ csv: SONDER_SUFFIX, SONDER_NAME
            for line in chapterPrefix:
                if delimiter + "KAPITEL-NUMMER" + delimiter in line:
                    result = chapter["KAPITEL_NR"]  #TODO harmonize name csv <-> template
                    line = line.replace(delimiter + "KAPITEL-NUMMER" + delimiter, result)
                if delimiter + "KAPITEL-DATUM" + delimiter in line:
                    result = chapter["DATUM"]   #TODO harmonize name csv <-> template
                    line = line.replace(delimiter + "KAPITEL-DATUM" + delimiter, result)
                if delimiter + "KAPITEL-UHRZEIT" + delimiter in line:
                    result = chapter["UHRZEIT"]   #TODO harmonize name csv <-> template
                    line = line.replace(delimiter + "KAPITEL-UHRZEIT" + delimiter, result)
                if delimiter + "PERSONEN" + delimiter in line:
                    result = chapter["PERSONEN"]
                    line = line.replace(delimiter + "PERSONEN" + delimiter, result)
                if delimiter + "EINLEITUNG" + delimiter in line:
                    result = chapter["EINLEITUNG"]
                    line = line.replace(delimiter + "EINLEITUNG" + delimiter, result)
                if delimiter in line :
                    print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
                outFile.writelines([line])

            for entry in entries[bookTitle]:
                # only print entries for this chapter/KB
                #TODO key error may arise for special suffixes etc. KAPITEL_NR here is misleading, it is actually NR+SPECIAL_SUFFIX if present
                if entry["KAPITEL_NR"] != chapter["KAPITEL_NR"]:
                    continue

                # entries; may contain VERS-VON, VERS-BIS, SPRECHER, INHALT  #TODO ??Überbegriff!Begriff?? für Stichwörter
                #TODO @ csv there is also: KAPITEL_NR - what to do with this?
                for line in entryTemplate:
                    #if delimiter + "" + delimiter in line:
                    #    result = chapter[""]
                    #    line = line.replace(delimiter + "" + delimiter, result)
                    if delimiter + "VERS-VON" + delimiter in line:
                        result = entry["VERS_VON"]
                        line = line.replace(delimiter + "VERS-VON" + delimiter, result)
                    if delimiter + "VERS-BIS" + delimiter in line:
                        result = entry["VERS_BIS"]
                        line = line.replace(delimiter + "VERS-BIS" + delimiter, result)
                    if delimiter + "SPRECHER" + delimiter in line:
                        result = entry["SPRECHER"]
                        line = line.replace(delimiter + "SPRECHER" + delimiter, result)
                    if delimiter + "INHALT" + delimiter in line:
                        result = entry["INHALT"]
                        # replace keyword markers
                        # NOTE: for LaTeX: !!keyword!! into \index{keyword}
                        numKeywordMarkers = result.count("!!")
                        if numKeywordMarkers > 0:
                            # sanity check
                            if numKeywordMarkers % 2 != 0:
                                print("FEHLER: Anzahl Ersetzungsfeld-Begrenzungen ('!!') ungerade in Inhalt von Eintrag KB {} V {} bis {}".format(entry["KAPITEL_NR"], entry["VERS_VON"], entry["VERS_BIS"]))
                            else:
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
                    if delimiter in line :
                        print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
                    outFile.writelines([line])

            # chapter postfix (no variables)
            outFile.writelines(chapterPostfix)

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
        if delimiter in line :
            print("WARNUNG: Unbekanntes Ersetzungsfeld in Zeile {}".format(line.rstrip()))
        outFile.writelines([line])

    # close output file
    outFile.close()
