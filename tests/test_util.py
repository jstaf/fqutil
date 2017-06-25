import fqutils.util as util

def test_prefix_extension():
    assert util.prefix_extension('r1.fastq', '_common') == 'r1_common.fastq'
    assert util.prefix_extension('r1.fastq.gz', '_common') == 'r1_common.fastq.gz'
    assert util.prefix_extension('tests/r1.fastq.gz', '_common') == 'tests/r1_common.fastq.gz'

def test_is_gzip():
    assert not util.is_gzip('tests/r1.fastq')
    assert util.is_gzip('tests/r1.fastq.gz')
