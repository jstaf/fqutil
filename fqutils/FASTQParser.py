#!/usr/bin/env python3

from numpy import array
import os, sys

# encoding symbols
encodings = {'sanger': '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHI',  # (0 - 40)
             'solexa64': ';<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh',  # (-5 - 40)
             'phred64_1.3': '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh',  # illumina 1.3+ (0 - 40)
             'phred64_1.5': 'BCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh',  # illumina 1.5+ (3 - 40)
             'phred33': '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJ'}  # illumina 1.8+ (0 - 41)
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

# convert letter encodings to numeric q values
def encoding2num(quals, encoding):
    quals = quals.replace('\n', '')
    numericQuals = []
    for char in quals:
        numericQuals.append(encodings[encoding].find(char))
    return array(numericQuals) + offsets[encoding]

class FASTQParser:
    # contents of the last read read
    read = {'header': '',
            'bases': '',
            'qheader': '',
            'quals': ''}
    numReads = 0

    def __init__(self, fileName):
        if os.path.isfile(fileName):
            self.fileName = fileName
            self.encoding = self.getFileEncoding()
            self.file = open(fileName, 'r')
        else:
            sys.exit('Invalid filename.')

    # determine file length and encoding by iterating through file q values
    def getFileEncoding(self):
        encodingList = []
        nLine = 0
        with open(self.fileName) as f:
            while True:
                line = f.readline()
                # detect EOF and break us out of loop
                if not line: break
                # also break loop if we've read more than 10000 reads, thats probably more than enough
                if nLine > 40000: break
                if nLine % 4 == 3:
                    encodingList.append(getLineEncoding(line))
                nLine += 1
        # okay have our per-line encodings, determine file encoding by looking for the presence of the most to least
        # restrictive encodings
        if 'phred33' in encodingList:
            encoding = 'phred33'
        elif 'sanger' in encodingList:
            encoding = 'sanger'
        elif 'solexa64' in encodingList:
            encoding = 'solexa64'
        elif 'phred64_1.3' in encodingList:
            encoding = 'phred64_1.3'
        else:
            encoding = 'phred64_1.5'
        return encoding

    def getFileLength(self):
        with open(self.fileName) as f:
            nlines = 0
            while True:
                # break at EOF
                if not f.readline():
                    break
                else:
                    nlines += 1
        return nlines

    def nextRead(self):
        self.read = {'header': self.file.readline(),
                     'bases': self.file.readline(),
                     'qheader': self.file.readline(),
                     'quals': self.file.readline()}
        self.numReads += 1
        return self.read

    def close(self):
        self.file.close()