import os
import sys
import gzip
from collections import OrderedDict

import fqutil


class Read:
    '''
    This class represents an individual fastq read. Importantly, this class
    does nothing to the underlying data unless specifically instructed to.
    '''

    # encoding symbols (quals, offset)
    encodings = {'phred64': (';<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi', -5),
                 'phred33': ('!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJ', 0)}
    # everything K+ and up is unique to phred64
    phred64_unique = set(encodings['phred64'][0][16:])

    
    def __init__(self, id, seq, quals, encoding='phred33'):
        self.id = id
        self.seq = seq
        self.quals = quals
        self.encoding = encoding

    
    def __str__(self):
        return self.seq.strip()

    
    def __repr__(self):
        return ''.join([self.id, self.seq, '+\n', self.quals])


    def write(self, handle):
        handle.writelines([self.id, self.seq, '+\n', self.quals])

    
    def unique_id(self):
        '''
        Get the unique identifier for a read without associated baggage.
        '''
        if '@SRR' in self.id:
            offset = 1
        else:
            offset = 0

        return self.id.split()[offset]


    def determine_encoding(self):
        '''
        Determine quality encoding of read. Note that this is not able to
        accurately determine encoding from one read. You should only use this
        method on many reads when trying to determine encoding from an unknown
        filetype.
        '''
        if len(Read.phred64_unique.intersection(self.quals)) > 0:
            return 'phred64'
        else:
            return 'phred33'


    def numeric_quals(self):
        '''
        Convert FASTQ quals to numeric Q values.
        '''
        enc = Read.encodings[self.encoding]  # for readability
        return [enc[0].find(char) + enc[1] for char in self.quals.strip()]


class Fastq:
    '''
    Helper class to rapidly parse fastq/gz as raw text. 
    (Biopython's Bio.SeqIO.index() does not support gzip compression :'( )
    '''

    def __init__(self, filename, mode='r', encoding=None):
        self.readno = 0
        self.filename = filename
        self.is_gzip = fqutil.is_gzip(self.filename)
        self.mode = mode
        if self.is_gzip:
            self.mode += 'b'
        
        self.handle = self.open()
        self.encoding = encoding
        if self.encoding is None and 'r' in mode:
            self.encoding = self.determine_encoding()

    
    def __enter__(self):
        return self

    
    def __exit__(self, typee, value, traceback):
        self.close()


    def open(self):
        '''
        Autodetect extension and return filehandle. Large (100MB) buffers are
        used to mitigate the impact of repeated write() calls. If encoding is
        unknown, it is determined from the file.
        '''
        handle = open(self.filename, self.mode, buffering=int(1e8)) 
        if self.is_gzip:
            handle = gzip.open(handle, self.mode)
        
        return handle


    def close(self):
        self.handle.close()


    def read(self):
        '''
        Gets the next fastq read. Returns None at EOF.
        '''
        # looks weird, but is faster than the old method
        if self.is_gzip:
            read = (
                self.handle.readline().decode(),
                self.handle.readline().decode(),
                self.handle.readline().decode(),
                self.handle.readline().decode()
            )
        else:
            read = (
                self.handle.readline(),
                self.handle.readline(),
                self.handle.readline(),
                self.handle.readline()
            )

        if read[0] == '':
            return None

        self.readno += 1
        return Read(read[0], read[1], read[3], encoding=self.encoding)

    
    def determine_encoding(self):
        '''
        Determine encoding by iterating through first 10000 read quals.
        '''
        self.seek(0)
        enclist = []
        for i in range(10000):
            read = self.read()
            if read is None:
                break
            else:
                enclist.append(read.determine_encoding())

        self.seek(0)
        if 'phred64' in enclist:
            return 'phred64'
        else:
            return 'phred33'


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


    def tell(self):
        self.handle.tell() 


    def to_dict(self):
        idx = OrderedDict()
        self.seek(0)
        while True:
            read = self.read()
            if read is None:
                break

            idx[read.unique_id()] = (read.seq, read.quals)

        return idx
