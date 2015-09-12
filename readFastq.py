__author__ = 'jeff'

# sanger encoding (0 - 40)
sanger = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHI'
# solexa64 encoding (-5 - 40)
solexa64 = ';<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh'
# phred64 (illumina 1.3+) (0-40)
phred64_1_3 = '@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh'
# phred64 (illumina 1.5+) (3-40)
phred64_1_5 = 'BCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh'
# phred33 (illumina 1.8+) (0-41)
phred33 = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJ'

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
assert('phred33' == getLineEncoding('@CCFDFFFHHHHHIJJIJJJJJJJJJJE@F:D?@DDGHB?BFHJJG8BGI###.-BDHDECHFHB?CEFEDEEDCDDDDDDCB?5@CDC@A?B<ACDD><A'))

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

        # okay have our per-line encodings, determine file encoding by looking for the most restrictive encodings
        if 'phred33' in encodingList: encoding = 'phred33'
        elif 'sanger' in encodingList: encoding = 'sanger'
        elif 'solexa64' in encodingList: encoding = 'solexa64'
        elif 'phred64_1.3' in encodingList: encoding = 'phred64_1.3'
        else: encoding = 'phred64_1.5'
    return encoding
assert(getFileEncoding(fileTest) == 'phred33')
