import fqutil

def test_prefix_extension():
    assert fqutil.prefix_extension('r1.fastq', '_common') == 'r1_common.fastq'
    assert fqutil.prefix_extension('r1.fastq.gz', '_common') == 'r1_common.fastq.gz'
    assert fqutil.prefix_extension('tests/r1.fastq.gz', '_common') == 'tests/r1_common.fastq.gz'


def test_is_gzip():
    assert not fqutil.is_gzip('tests/r1.fastq')
    assert fqutil.is_gzip('tests/r1.fastq.gz')
