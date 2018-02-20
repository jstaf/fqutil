from fqutil import Fastq, Read

def test_read_encoding_detection():
    p64 = Read.encodings['phred64'][0]
    phred64 = Read(id='@phred64:example\n', seq='A' * len(p64), quals=p64)
    assert phred64.determine_encoding() == 'phred64'
    
    p33 = Read.encodings['phred33'][0]
    phred33 = Read(id='@phred33:example\n', seq='A' * len(p33), quals=p33)
    assert phred33.determine_encoding() == 'phred33'
    

def test_fastq_encoding_detection():
    assert Fastq('tests/r1.fastq').encoding == 'phred33'
    assert Fastq('tests/r2.fastq').encoding == 'phred33'


def test_fastq_to_dict():
    with Fastq('tests/r1.fastq') as fq:
        idx = fq.to_dict()
    
    read = idx['@D00707:124:C9VMNANXX:4:2108:4864:36753'] 
    assert read[0] == 'CACGCGGGCAAAGGCTCCTCCGGGCCCCTCACCAGCCCCAGGTCTTTTCCCAGAGATGCCCTTGCGCCTCATGACCAGCTTGTTGAAGAGATCCGACATCAAGTGCCCACCTTGGCTCGTGGCTC\n'
    assert read[1] == 'BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFFFFFFFFFFFFFF<\n'
