#!/usr/bin/env python3

# This script will compare two FASTQ files and find and separate paired/nonpaired reads. Basically a replacement for
# cmpfastq.perl, which seems to have a 100% crash rate if given a large file (in my experience at least).

__author__ = 'jeff'

import sys, getopt, os, re
from FASTQParser import *

helpString = '\nUsage:\n\nmatchFASTQ -1 <fastqFile1> -2 <fastqFile2>\n'

def main(argv):
    fastq1 = ''
    fastq2 = ''
    rexp = '\w+:\w+\s'
    outDir = 'matchOut'
    opts, args = getopt.getopt(argv[1:], '1:2:ho:r:', 'help')
    for opt, val in opts:
        if opt == '-1':
            fastq1 = val
        elif opt == '-2':
            fastq2 = val
        elif opt in ['-h', '--help']:
            sys.exit(helpString)
        elif opt == '-o':
            outDir = val
        elif opt == '-r':
            rexp = val
        else:
            sys.exit('Unsupported parameter')
    if fastq1 == '' or fastq2 == '':
        print(helpString)
        sys.exit('Requires two valid input files.')

    global regex
    regex = re.compile(rexp)

    os.mkdir(outDir)
    matchReads(fastq1, fastq2, outDir)

# function prototype
def matchReads(toMatch, matchAgainst, outDir):
    idxParser = FASTQParser(matchAgainst)

    # read file, retrieve read names for 100000 reads, dump to temp file, store in dict that says in which file the read
    #  is. We will later retrieve matched reads based on this dictionary
    last = -1
    nread = 10000000000 # to force file creation
    tmpFile = None
    IDStore = {}
    try:
        while True:
            # open new tmp file and reset
            if nread > 100000:
                nread = 0
                last += 1
                if tmpFile is not None:
                    tmpFile.close()
                #TODO double check the path filenaming conventions
                tmpFile = open(outDir + '/' + toMatch + '.' + str(last), mode='bw')

            # process individual reads
            read = idxParser.nextRead()
            # break at EOF
            if read['quals'] == '':
                break
            # qual header is lost to save space (all it needs to be is a '+' anyways...)
            tmpFile.writelines([read['header'], read['bases'], read['quals']])
            # get tile X/Y position and use as key for dictionary that stores the file# and line# for later use with
            #  linecache
            IDStore[regex.findall(read['header'])[1]] = (last, nread)
            nread += 1
    finally:
        idxParser.close()

    toMatchParser = FASTQParser(toMatch)
    while True:
        read = toMatchParser.nextRead()

if __name__ == '__main__':
    main(sys.argv)