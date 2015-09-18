#!/usr/bin/env python3

__author__ = 'jeff'

import sys, getopt, os
from FASTQParser import *

helpString = '\nUsage:\n\nFASTQTrimmer_.py [-q <minReadQual>] [-o <outputfile>] <inputFile>\n'


def main(argv):
    # parse arguments
    opts, args = getopt.getopt(argv[1:-1], 'ho:q:', longopts = ['help'])

    qmin = 30
    outputName = ''

    for option, val in opts:
        if option in ['-h', '--help']:
            print(helpString)
            sys.exit()
        elif option == '-o':
            outputName = val
        elif option == '-q':
            qmin = float(val)
        else:
            sys.exit('Unsupported parameter.')
    # deal with invalid paths
    if (len(argv) == 1) or (not os.path.isfile(argv[-1])):
        print(helpString)
        sys.exit('Valid input file required.')
    else:
        inputName = argv[-1]

    parser = FASTQParser(inputName)
    if outputName != '':
        outFile = open(outputName, 'w')
    # read file and print back lines that pass the filter
    while True:
        read = parser.nextRead()
        # stop at EOF
        if read['quals'] == '':
            break
        numQual = encoding2num(read['quals'], parser.encoding)
        # get first index of acceptable quality
        start = -1
        for baseq in numQual:
            start += 1
            if baseq >= qmin:
                break
        # now get last index
        end = -1
        for baseq in reversed(numQual):
            end += 1
            if baseq >= qmin:
                break
        # only print back reads where there was at least one decent base call
        end = len(numQual) - end - 1
        if start < end:
            if outputName == '':
                print(read['header'], read['bases'][start:end], '\n', read['qheader'], read['quals'][start:end], '\n',\
                      sep='', end='')
            else:
                outFile.writelines([read['header'], read['bases'][start:end], '\n', \
                                    read['qheader'], read['quals'][start:end], '\n'])
    parser.file.close()
    if outputName != '':
        outFile.close()

if __name__ == '__main__':
    main(sys.argv)