#!/usr/bin/python3

from numpy import *

testQual = '@CCFDFFFHHHHHIJJIJJJJJJJJJJE@F:D?@DDGHB?BFHJJG8BGI###.-BDHDECHFHB?CEFEDEEDCDDDDDDCB?5@CDC@A?B<ACDD><A'
qmin = 30

# encoding symbols
encodings = {'sanger': '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHI', # (0 - 40)
             'solexa64': ';<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh', # (-5 - 40)
             'phred64_1.3': '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh', # illumina 1.3+ (0 - 40)
             'phred64_1.5': 'BCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh', # illumina 1.5+ (3 - 40)
             'phred33': '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJ'} # illumina 1.8+ (0 - 41)
# encoding offsets
offsets = {'sanger': 0,
           'solexa64': -5,
           'phred64_1.3': 0,
           'phred64_1.5': 3,
           'phred33': 0}

# determine quality encoding of line, needs to read a whole bunch of lines or else you end up with phred64_1.5 by default
def getLineEncoding(quals):
    if '#' in quals:
        if 'J' in quals:
            encoding = 'phred33'
        else:
            encoding = 'sanger'
    else:
        if ';' in quals:
            encoding = 'solexa64'
        elif '@' in quals:
            encoding = 'phred64_1.3'
        else:
            encoding = 'phred64_1.5'
    return encoding
# test
assert(getLineEncoding(testQual) == 'phred33')

fileTest = 'uber_short.fastq'

def getFileLength(fileName):
    with open(fileName) as file:
        nlines = 0
        while True:
            # break at EOF
            if not file.readline():
                break
            else:
                nlines += 1
    return nlines
# test
assert(getFileLength(fileTest) == 100)

# determine file length and encoding by iterating through file q values
def getFileEncoding(fileName):
    encodingList = []
    with open(fileName) as file:
        nLine = 0

        while True:
            line = file.readline()
            # detect EOF and break us out of loop
            if not line: break
            # also break loop if we've read more than 1000000 lines, thats probably more than enough
            if nLine > 100000: break
            if nLine % 4 == 3:
                encodingList.append(getLineEncoding(line))
            nLine += 1

        # okay have our per-line encodings, determine file encoding by looking for the presence of the most to least
        # restrictive encodings
        if 'phred33' in encodingList: encoding = 'phred33'
        elif 'sanger' in encodingList: encoding = 'sanger'
        elif 'solexa64' in encodingList: encoding = 'solexa64'
        elif 'phred64_1.3' in encodingList: encoding = 'phred64_1.3'
        else: encoding = 'phred64_1.5'
    return encoding
assert(getFileEncoding(fileTest) == 'phred33')

# convert letter encodings to numeric q values
def encoding2num(quals, encoding):
    quals = quals.replace('\n', '')
    numericQuals = []
    for char in quals:
        numericQuals.append(encodings[encoding].find(char))
    return array(numericQuals) - offsets[encoding]

def parseFile(fileName):
    enc = getFileEncoding(fileName)

    header = ''
    def setHeader(content):
        nonlocal header
        header = content
        return 0
    bases = ''
    def setBases(content):
        nonlocal bases
        bases = content
        return 0
    qHeader = ''
    def setQHeader(content):
        nonlocal qHeader
        qHeader = content
        return 0
    quals = ''
    def setQuals(content):
        nonlocal quals
        quals = content
        return mean(encoding2num(content, enc))

    # open file and only write reads to console if they meet certain quality values
    nLine = 0
    with open(fileName) as file:
        while True:
            line = file.readline()
            if not line: break

            n = nLine % 4

            switch = {0: setHeader,
                      1: setBases,
                      2: setQHeader,
                      3: setQuals}
            qstat = switch[n](line)

            # do we filter out this value?
            if (n == 3) and (qstat >= qmin):
                # dump to console
                print(header, bases, qHeader, quals, sep = '', end = '')

            nLine += 1;

parseFile(fileTest)