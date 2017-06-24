import unittest

import fqutils.fastq as fastq
import fqutils.util as util

class Fastq(unittest.TestCase):

    def test_prefix_extension_single(self):
        self.assertEqual(util.prefix_extension('r1.fastq', '_common'),
            'r1_common.fastq')

    def test_prefix_extension_double(self):
        self.assertEqual(util.prefix_extension('r1.fastq', '_common'),
            'r1_common.fastq')

