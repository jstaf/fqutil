import fqutils.fastq as fastq
import fqutils.util as util

def test_prefix_extension_single():
    assert util.prefix_extension('r1.fastq', '_common') == 'r1_common.fastq'

def test_prefix_extension_double():
    assert util.prefix_extension('r1.fastq.gz', '_common') == 'r1_common.fastq.gz'

