"""A helper class with some fastq parsing methods"""

import os
import sys
import re
import gzip

class Fastq:
    """
    Helper class to rapidly parse fastq/gz as raw text. 
    (Biopython's Bio.SeqIO.index() does not support gzip compression :'( )
    """

    pos = None

    def __init__(self, filename, mode='r'):
        if not os.path.isfile(filename):
            sys.exit('%s is not a valid file path.' % filename)
        self.filename = filename
        self.mode = mode
        self.handle = self.open()

    
    def __enter__(self):
        pass  # handle is already open

    
    def __exit__(self, typee, value, traceback):
        self.close()

    
    def is_gzip(self):
        return len(re.findall(r'.gz$', self.filename)) > 0


    def open(self):
        """
        Autodetect extension and return filehandle.
        """
        if self.is_gzip():
            self.mode = self.mode + 'b'
            return gzip.open(self.filename, mode=self.mode)
        else:
            return open(self.filename, self.mode)


    def close(self):
        self.handle.close()


    def get_read(self):
        """Get a fastq read. Returns None at EOF"""
        self.pos = self.handle.tell()
        read = []
        for i in range(4):  # assumes 4-line FASTQ
            line = self.handle.readline()
            if line == '':
                return None  # EOF
            read.append(line)
        return read


    def write(self, read):
        self.handle.writelines(read)

    
    def seek(self, position):
        """Jump to a particular file position"""
        self.handle.seek(position)


