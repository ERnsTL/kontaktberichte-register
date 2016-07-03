#!/usr/bin/env python3

"""Setzt ein Register der Kontaktberichte von Billy Meier in Form einer
weiterverarbeitbaren Quelldatei (LaTeX oder HTML) zusammen."""

import argparse
from enum import Enum
from collections import deque
import sys

class TemplateState(Enum):
    TemplatePrefix = 1  # looking for book begin
    BookPrefix = 2  # looking for chapter begin
    EntryPrefix = 3 # looking for entry begin
    Entry = 4   # looking for entry end
    ChapterPostfix = 5   # looking for chapter end
    BookPostfix = 6 # looking for book end
    TemplatePostfix = 7 # looking for template end

if __name__ == '__main__':
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
    parser.add_argument("-o", "--output", type=str, help="output file path", default="register.tex")
    parser.add_argument("-V", "--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        print("Version: 0.0.1 (2016-07-03)")
        sys.exit(0)
    #print("OK, generiere {}".format(args.format))

    # parse template line by line, resulting in static parts and dynamic parts
    filename = ("main.tex" if args.format == "latex" else "index.html")
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
    templatePrefix = deque([])
    templatePostfix = deque([])
    bookPrefix = []
    bookPostfix = []
    chapterPrefix = []
    chapterPostfix = []
    entryTemplate = []
    for line in templateFile:
        if state == TemplateState.TemplatePrefix:
            if "%%BUCH_ANFANG%%" in line:
                # NOTE: discarding line
                state = TemplateState.BookPrefix
            else:
                # still in template prefix, save line
                templatePrefix.append(line)
        elif state == TemplateState.BookPrefix:
            if "%%KAPITEL_ANFANG%%" in line:
                # NOTE: discarding line
                state = TemplateState.EntryPrefix
            else:
                # still in book prefix, save line
                bookPrefix.append(line)
        elif state == TemplateState.EntryPrefix:
            if "%%EINTRAG_ANFANG%%" in line:
                # NOTE: discard line
                state = TemplateState.Entry
            else:
                # still in entry, save line
                chapterPrefix.append(line)
        elif state == TemplateState.Entry:
            if "%%EINTRAG_ENDE%%" in line:
                # NOTE: discard line
                state = TemplateState.ChapterPostfix
            else:
                # still after entry in chapter, save line
                entryTemplate.append(line)
        elif state == TemplateState.ChapterPostfix:
            if "%%KAPITEL_ENDE%%" in line:
                # NOTE: discard line
                state = TemplateState.BookPostfix
            else:
                # still after chapter in book, save line
                chapterPostfix.append(line)
        elif state == TemplateState.BookPostfix:
            if "%%BUCH_ENDE%%" in line:
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
            print("FEHLER: Unbekannter Zustand {}".format(state))
            sys.exit(2)
    templateFile.close()
    if state != TemplateState.TemplatePostfix:
        #TODO better warning message: which marker was not found?
        which = "ERROR"
        if state == TemplateState.TemplatePrefix:
            which = "%%BUCH_ANFANG%%"
        elif state == TemplateState.BookPrefix:
            which = "%%KAPITEL_ANFANG%%"
        elif state == TemplateState.EntryPrefix:
            which = "%%EINTRAG_ANFANG%%"
        elif state == TemplateState.Entry:
            which = "%%EINTRAG_ENDE%%"
        elif state == TemplateState.ChapterPostfix:
            which = "%%KAPITEL_ENDE%%"
        elif state == TemplateState.BookPostfix:
            which = "%%BUCH_ENDE%%"
        elif state == TemplateState.TemplatePostfix:
            which = "EOF"   # NOTE: should never happen
        print("FEHLER: Markierung {} fehlt in der Vorlage -> Markierungen auf Vollständigkeit überprüfen.".format(which))
        sys.exit(3)

    # enerate output file
    outFile.writelines(templatePrefix)
    outFile.writelines(bookPrefix)
    outFile.writelines(chapterPrefix)
    outFile.writelines(entryTemplate)
    outFile.writelines(chapterPostfix)
    outFile.writelines(bookPostfix)
    outFile.writelines(templatePostfix)
    #TODO outFile.write(line.replace('old_text', 'new_text'))
    #TODO templatePrefix.popleft()
    outFile.close()
