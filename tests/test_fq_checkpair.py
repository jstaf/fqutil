"""Check that fq-checkpair is properly detecting mismatched reads"""

import os

def test_are_mismatched():
    assert not os.system('./fq-checkpair tests/r1.fastq tests/r2.fastq') == 0


def test_are_mismatched_gz():
    assert not os.system('./fq-checkpair tests/r1.fastq.gz tests/r2.fastq.gz') == 0


def test_are_matched():
    assert os.system('./fq-checkpair tests/r1_cmn.fastq tests/r2_cmn.fastq') == 0


def test_are_matched_gz():
    assert os.system('./fq-checkpair tests/r1_cmn.fastq.gz tests/r2_cmn.fastq.gz') == 0
