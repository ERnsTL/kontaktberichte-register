#!/usr/bin/env python3

"""Setzt ein Register der Kontaktberichte von Billy Meier in Form einer
weiterverarbeitbaren Quelldatei (LaTeX oder HTML) zusammen."""

import argparse
from enum import Enum
from collections import deque

class TemplateState(Enum):
    LookingForBookBegin = 1
    LookingForChapterBegin = 2
    LookingForEntryBegin = 3
    LookingForEntryEnd = 4
    LookingForChapterEnd = 5
    LookingForBookEnd = 6
    LookingForTemplateEnd = 7

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
        return
    print("OK, generiere {}".format(args.format))

    # parse template line by line, resulting in static parts and dynamic parts
    filename = ("main.tex" if args.format == "latex" else "index.html")
    templateFile = open("./vorlagen/{}/{}".format(args.template, filename), 'r')
    outFile = open(args.output, 'w')
    state = TemplateState.LookingForBookBegin
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
    bookPrefix = deque([])
    bookPostfix = deque([])
    chapterPrefix = []
    chapterPostfix = []
    entryTemplate = []
    for line in templateFile:
        if state == TemplateState.LookingForBookBegin:
            if "%%BUCH_ANFANG%%" in line:
                # NOTE: discards line
                state = TemplateState.LookingForChapterBegin
            else:
                templatePrefix.append(line)
        elif state == TemplateState.LookingForChapterBegin:
            #TODO
        elif state == TemplateState.LookingForEntryBegin:
            #TODO
        elif state == TemplateState.LookingForEntryEnd:
            #TODO
        elif state == TemplateState.LookingForChapterEnd:
            #TODO
        elif state == TemplateState.LookingForBookEnd:
            #TODO
        elif state == TemplateState.LookingForTemplateEnd:
            #TODO
        else:
            print("FEHLER: Unbekannter Zustand {}".format(state))
    templateFile.close()

    # Generate output file
    # template prefix (static)
    #TODO outFile.write(line.replace('old_text', 'new_text'))
    #TODO templatePrefix.popleft()
    # template postfix (static)
    outFile.close()
