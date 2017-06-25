"""Check that reads are being properly repaired"""

import os
import glob

def delete_test_files(extension):
    testfiles = glob.glob('tests/*_*' + extension)
    for f in list(filter(lambda f: 'cmn' not in f, testfiles)):
        os.unlink(f)


def test_repair():
    delete_test_files('.fastq')
    os.system('./fq-repair -u tests/r1.fastq tests/r2.fastq')
    assert os.path.isfile('tests/r1_common.fastq')
    assert os.path.isfile('tests/r2_common.fastq')
    assert os.system('./fq-checkpair tests/r1_common.fastq tests/r2_common.fastq') == 0
    assert os.path.isfile('tests/r1_unique.fastq')
    assert os.path.isfile('tests/r2_unique.fastq')
    assert os.system('./fq-checkpair tests/r1_unique.fastq tests/r2_unique.fastq') == 256


def test_repair_gz():
    delete_test_files('.fastq.gz')
    os.system('./fq-repair -u tests/r1.fastq.gz tests/r2.fastq.gz')
    assert os.path.isfile('tests/r1_common.fastq.gz')
    assert os.path.isfile('tests/r2_common.fastq.gz')
    assert os.system('./fq-checkpair tests/r1_common.fastq.gz tests/r2_common.fastq.gz') == 0
    assert os.path.isfile('tests/r1_unique.fastq.gz')
    assert os.path.isfile('tests/r2_unique.fastq.gz')
    assert os.system('./fq-checkpair tests/r1_unique.fastq.gz tests/r2_unique.fastq.gz') == 256
