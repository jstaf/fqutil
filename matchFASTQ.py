#!/usr/bin/env python3

# This script will compare two FASTQ files and find and separate paired/nonpaired reads. Basically a replacement for
# cmpfastq.perl, which seems to have a 100% crash rate if given a large file (in my experience at least).

__author__ = 'jeff'

import sys, getopt, os
from FASTQParser import *

helpString = '\nUsage:\n\nmatchFASTQ -1 <fastqFile1> -2 <fastqFile2>\n'

def main(argv):
    fastq1 = ''
    fastq2 = ''
    outDir = 'matchOut'
    opts, args = getopt.getopt(argv[1:], '1:2:ho:', 'help')
    for opt, val in opts:
        if opt == '-1':
            fastq1 = val
        elif opt == '-2':
            fastq2 = val
        elif opt in ['-h', '--help']:
            sys.exit(helpString)
        elif opt == '-o':
            outDir = val
        else:
            sys.exit('Unsupported parameter')
    if fastq1 == '' or fastq2 == '':
        print(helpString)
        sys.exit('Requires two valid input files.')

    os.mkdir(outDir)
    matchReads(fastq1, fastq2, outDir)
    matchReads(fastq2, fastq1, outDir)

# function prototype
def matchReads(toMatch, matchAgainst, outDir):
    pass

if __name__ == '__main__':
    main(sys.argv)