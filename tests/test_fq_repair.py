"""Check that reads are being properly repaired"""

import os
import shutil
import glob

import pytest


def delete_test_files(extension):
    testfiles = glob.glob('tests/*_*' + extension)
    for f in list(filter(lambda f: 'cmn' not in f, testfiles)):
        os.unlink(f)


def test_post_py34_fix():
    '''
    Do we avoid the post exist_ok removal without errors.
    '''
    assert os.system('cd tests && ../fq-repair -u r1.fastq r2.fastq') == 0


@pytest.fixture
def test_repair_mixed():
    '''
    Test normal functionality when reads are both common and unique.
    '''

    delete_test_files('.fastq')
    assert os.system('./fq-repair -u tests/r1.fastq tests/r2.fastq') == 0
    assert os.path.isfile('tests/r1_common.fastq')
    assert os.path.isfile('tests/r2_common.fastq')
    assert os.path.isfile('tests/r1_unique.fastq')
    assert os.path.isfile('tests/r2_unique.fastq')
    # check uniqueness using fq-checkpair    
    assert not os.system('./fq-checkpair tests/r1_unique.fastq tests/r2_unique.fastq') == 0
    assert os.system('./fq-checkpair tests/r1_common.fastq tests/r2_common.fastq') == 0


def test_repair_all_common(test_repair_mixed):
    '''
    When all reads are common, no reads should be unique.
    '''

    assert os.system('./fq-repair -u tests/r1_common.fastq tests/r2_common.fastq') == 0
    # should be no unique reads
    assert os.path.getsize('tests/r1_common_unique.fastq') == 0
    assert os.path.getsize('tests/r2_common_unique.fastq') == 0 


def test_repair_all_unique(test_repair_mixed):
    '''
    When all reads are unique, no reads should be common.
    '''

    assert os.system('./fq-repair -u tests/r1_common.fastq tests/r2_common.fastq') == 0
    # should be no common reads
    assert os.path.getsize('tests/r1_common_unique.fastq') == 0
    assert os.path.getsize('tests/r2_common_unique.fastq') == 0 


def test_repair_gz():
    '''
    Does the script work on gzipped files?
    '''

    delete_test_files('.fastq.gz')
    assert os.system('./fq-repair -u tests/r1.fastq.gz tests/r2.fastq.gz') == 0
    assert os.path.isfile('tests/r1_common.fastq.gz')
    assert os.path.isfile('tests/r2_common.fastq.gz')
    assert os.path.isfile('tests/r1_unique.fastq.gz')
    assert os.path.isfile('tests/r2_unique.fastq.gz')
    # check results using fq-checkpair
    assert os.system('./fq-checkpair tests/r1_common.fastq.gz tests/r2_common.fastq.gz') == 0
    assert not os.system('./fq-checkpair tests/r1_unique.fastq.gz tests/r2_unique.fastq.gz') == 0


def test_repair_outdir():
    '''
    Does the output directory functionality work?
    '''

    shutil.rmtree('./tests/outdir', ignore_errors=True)
    assert os.system('./fq-repair -o tests/outdir/works -u tests/r1.fastq tests/r2.fastq') == 0
    assert os.path.isfile('tests/outdir/works/r1_common.fastq')
    assert os.path.isfile('tests/outdir/works/r2_common.fastq')
    assert os.path.isfile('tests/outdir/works/r1_unique.fastq')
    assert os.path.isfile('tests/outdir/works/r2_unique.fastq')

