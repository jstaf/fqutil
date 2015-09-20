#!/usr/bin/env python3

# This script will compare two FASTQ files and find and separate paired/nonpaired reads. Basically a replacement for
# cmpfastq.perl, which seems to have a 100% crash rate if given a large file (in my experience at least).

__author__ = 'jeff'

import sys, getopt, os, re
from FASTQParser import *

# defaults, edit if you're feeling brave.
helpString = '\nUsage:\n\nmatchFASTQ -1 <fastqFile1> -2 <fastqFile2> [-r "alternate regular expression to parse read header"]\n'
fastq1 = ''
fastq2 = ''
rexp = '\w+:\w+\s'

def main(argv):
    opts, args = getopt.getopt(argv[1:], '1:2:hr:', 'help')
    for opt, val in opts:
        if opt == '-1':
            fastq1 = val
        elif opt == '-2':
            fastq2 = val
        elif opt in ['-h', '--help']:
            sys.exit(helpString)
        elif opt == '-r':
            rexp = val
        else:
            sys.exit('Unsupported parameter')
    if fastq1 == '' or fastq2 == '':
        print(helpString)
        sys.exit('Requires two valid input files.')

    global regex
    regex = re.compile(rexp)

    matchReads(fastq1, fastq2)
    return

def indexFile(fileName):
    idxParser = FASTQParser(fileName)

    IDStore = {}
    try:
        while True:
            # process individual reads
            pos = idxParser.file.tell()
            read = idxParser.nextRead()
            # break at EOF
            if read['quals'] == '':
                break
            # get tile X/Y position and use as key for dictionary that stores file position for later read
            IDStore[regex.findall(read['header'])[0]] = pos
    finally:
        idxParser.close()
    return IDStore

def matchReads(fastq1, fastq2):
    idxStore = indexFile(fastq1)

    # open file handles
    fastq1_common = open(fastq1 + '.common', 'w')
    fastq1_unique = open(fastq1 + '.unique', 'w')
    fastq2_common = open(fastq2 + '.common', 'w')
    fastq1_parser = FASTQParser(fastq1)
    fastq2_parser = FASTQParser(fastq2)
    while True:
        read = fastq1_parser.nextRead()
        # EOF
        if read['quals'] == '':
            break
        ID = regex.findall(read['header'])[0]
        if ID in idxStore:
            # write both reads out to common files, remove key from index
            fastq1_common.writelines([read['header'], read['bases'], read['qheader'], read['quals']])

            fastq2_parser.file.seek(idxStore.pop(ID))
            readMatch = fastq2_parser.nextRead()
            fastq2_common.writelines([readMatch['header'], readMatch['bases'], readMatch['qheader'], readMatch['quals']])
        else:
            # write out to unique file for fastq1
            fastq1_unique.writelines([read['header'], read['bases'], read['qheader'], read['quals']])
    # close file handles
    fastq1_common.close()
    fastq1_unique.close()
    fastq2_common.close()

    # all remaining keys in dictionary are the unique reads for fastq2
    with open(fastq2 + '.unique', 'w') as fastq2_unique:
        for remaining in idxStore:
            fastq2_parser.file.seek(idxStore[remaining])
            read = fastq2_parser.nextRead()
            fastq2_unique.writelines([read['header'], read['bases'], read['qheader'], read['quals']])
    return

if __name__ == '__main__':
    main(sys.argv)