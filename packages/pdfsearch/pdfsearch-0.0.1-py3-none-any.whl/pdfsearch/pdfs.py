#!/usr/bin/env python


import argparse
import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.high_level import extract_text
from pathlib import Path


def contains_keyword(path, keyw, verb, npages, title, infok):
    ''' Search in the directory path for pdf metadata containing the keyword
        keyw or search the first n pages of the document
        or search the keyw in the filename of the file
    '''

    if not (npages or title or infok):
        # if no options are set, make searching in the filename
        # the default behaviour
        title = True
    try:
        for file in path[0].iterdir():
            if file.suffix == '.pdf':
                if title:
                    if keyw[0].lower() in str(file.name).lower():
                        yield str(file.as_uri()).replace(' ', '%20')
                        continue
                if infok or npages:
                    with file.open('rb') as f:
                        pdfP = PDFParser(f)
                        doc = PDFDocument(pdfP)
                        if infok:
                            info = doc.info
                            try:
                                if keyw[0].lower() in\
                                        str(info[0]['Keywords']).lower():
                                    yield (str(file.as_uri()).replace(' ',
                                                                      '%20'))
                                    continue
                            except KeyError as kexc:
                                if verb:
                                    yield ("[!] No Keywords attribute in"
                                           " info document in "
                                           + str(file)+" "+str(kexc))
                                else:
                                    pass
                            except IndexError as Iexc:
                                if verb:
                                    if not info:
                                        yield ("[!] No Info document"
                                               " available on "+str(file)
                                               + " "+str(Iexc))
                                else:
                                    pass
                        if npages:
                            try:
                                txt = extract_text(f, maxpages=npages)
                                if keyw[0].lower() in txt.lower():
                                    yield(str(file.as_uri()).replace(' ',
                                                                     '%20'))
                            except IndexError as Iexc:
                                if verb:
                                    yield(str(Iexc))
                                pass
    except OSError as exc:
        if verb:
            print("[!]"+str(exc))
        pass


def Main(argv):
    parser = argparse.ArgumentParser(description="Searchs for pdf files in a"
                                     "folder containing a keyword in metadata"
                                     ", filenames or an arbitray number of "
                                     "start pages.\n If no options are "
                                     "selected searching in the filename is "
                                     "the default.")
    parser.add_argument('--directory', '-d', nargs=1, default=[Path.cwd()],
                        type=Path, help="specifies the path to search. If not"
                        "set, the default is the current directory.")
    parser.add_argument('--verbose', '-v', action='store_true',
                        help=("Shows additional information about not existing"
                              " info documents or keyword attributes"))
    parser.add_argument('--filename', '-f', action='store_true',
                        help=("Searches the filenames of pdf files for the "
                              "keyword"))
    parser.add_argument('--npages', '-n', nargs='?', const=3, type=int,
                        help="Search the first n pages of the pdf file for "
                        "the keyword")
    parser.add_argument('--infok', '-k', action='store_true',
                        help=("Searches the keyword in the keywords-entry in "
                              "the metadata of the document"))

    parser.add_argument('keyword', nargs=1, help="the keyword to search for")
    args = parser.parse_args(argv[1:])

    for i in contains_keyword(args.directory, args.keyword, args.verbose,
                              args.npages, args.filename, args.infok):
        print(i)

    return 0


if __name__ == "__main__":
    Main(sys.argv)
