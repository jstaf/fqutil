import os
import sys
import gzip

import fqutils.util as util

class Fastq:
    """
    Helper class to rapidly parse fastq/gz as raw text. 
    (Biopython's Bio.SeqIO.index() does not support gzip compression :'( )
    """

    pos = 0
    lineno = 0
    tempfilename = None

    def __init__(self, filename, mode='r'):
        if 'r' in mode and not os.path.isfile(filename):
            sys.exit('%s is not a valid file path.' % filename)
        self.filename = filename
        self.mode = mode
        self.is_gzip = util.is_gzip(self.filename)
        self.handle = self._open()

    
    def __enter__(self):
        return self

    
    def __exit__(self, typee, value, traceback):
        self.close()


    def _open(self):
        """
        Autodetect extension and return filehandle.
        """
        if self.is_gzip:
            self.mode = self.mode + 'b'
            return gzip.open(self.filename, mode=self.mode)
        else:
            return open(self.filename, self.mode)


    def close(self):
        """Close file handles and delete tempspace if it exists."""
        self.handle.close()
        if self.tempfilename is not None:
            os.unlink(self.tempfilename)


    def get_read(self):
        """Get a fastq read. Returns None at EOF"""
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


    def writelines(self, read):
        """Same thing as the "normal" writelines"""
        if self.is_gzip:
            read = [b.encode() for b in read]
        self.handle.writelines(read)

    
    def seek(self, position):
        """Jump to a particular file position"""
        self.handle.seek(position)
        self.pos = position


    def index(self):
        """
        Create a dictionary of readids and their seek positions.
        Autodumps gzipped files to raw fastq to allow random access.
        """
        
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
            self.lineno = 0
        return idx
