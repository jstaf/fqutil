import os
import sys
import gzip

import fqutil

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


def get_line_encoding(quals):
    '''
    Determine quality encoding of line. 
    It is not sufficient to run this on a single line to determine a file's encoding.
    '''
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


def encoding2num(quals, encoding):
    '''
    Convert FASTQ quals to numeric Q values
    '''
    quals = quals.replace('\n', '')
    numeric_quals = []
    for char in quals:
        numeric_quals.append(encodings[encoding].find(char) + offsets[encoding])

    return numeric_quals


class Fastq:
    '''
    Helper class to rapidly parse fastq/gz as raw text. 
    (Biopython's Bio.SeqIO.index() does not support gzip compression :'( )
    '''

    pos = 0
    lineno = 0
    tempfilename = None

    def __init__(self, filename, mode='r'):
        if 'r' in mode and not os.path.isfile(filename):
            sys.exit('%s is not a valid file path.' % filename)
        self.filename = filename
        self.mode = mode
        self.is_gzip = fqutil.is_gzip(self.filename)
        self.handle = self._open()

    
    def __enter__(self):
        return self

    
    def __exit__(self, typee, value, traceback):
        self.close()


    def _open(self):
        '''
        Autodetect extension and return filehandle.
        '''
        if self.is_gzip:
            self.mode = self.mode + 'b'
            return gzip.open(self.filename, mode=self.mode)
        else:
            return open(self.filename, self.mode)


    def close(self):
        '''
        Close file handles and delete tempspace if it exists.
        '''
        self.handle.close()
        if self.tempfilename is not None:
            os.unlink(self.tempfilename)


    def get_read(self):
        '''
        Get a fastq read. Returns None at EOF.
        '''
        self.pos = self.handle.tell()
        read = []
        for i in range(4):  # assumes 4-line FASTQ
            line = self.handle.readline()
            if self.is_gzip:
                line = line.decode()
            if line == '' or line == b'':
                return None  # EOF
            read.append(line)
        self.lineno += 1
        return read

    
    def get_encoding(self):
        '''
        Determine encoding by iterating through first 10000 read quals.
        '''
        startpos = self.pos
        self.seek(0)
        enclist = []
        for i in range(10000):
            read = self.get_read()
            if read is None:
                break
            else:
                enclist.append(read[2])
        self.seek(startpos)

        # determine file encoding by looking for the presence of the most to least
        # restrictive encodings
        if 'phred33' in enclist:
            return 'phred33'
        elif 'sanger' in enclist:
            return 'sanger'
        elif 'solexa64' in enclist:
            return 'solexa64'
        elif 'phred64_1.3' in enclist:
            return 'phred64_1.3'
        else:
            return 'phred64_1.5'


    def writelines(self, read):
        '''
        Same thing as the "normal" writelines.
        '''
        if self.is_gzip:
            read = [b.encode() for b in read]
        self.handle.writelines(read)

    
    def seek(self, position):
        '''
        Jump to a particular file position.
        '''
        self.handle.seek(position)
        self.pos = position


    def index(self):
        '''
        Create a dictionary of readids and their seek positions.
        Autodumps gzipped files to raw fastq to allow random access.
        '''
        
        self.seek(0)
        if self.is_gzip:
            # initialize raw fastq temp space
            self.tempfilename = self.filename + '.temp'
            temp = open(self.tempfilename, mode='w+')
        
        # build index
        idx = {}
        while True:
            read = self.get_read()
            if read is None:
                break
            else:
                idx[read[0]] = self.pos
                if self.is_gzip:
                    temp.writelines(read)
        if self.is_gzip:
            # the tempfile is now used in place of original file handle
            self.handle.close()
            self.handle = temp
            self.seek(0)
            self.is_gzip = False

        # indexing should not count lines in file
        self.lineno = 0
        return idx

