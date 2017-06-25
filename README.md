# fqutils

A couple Python-based FASTQ QC tools that perform several useful file handling operations, 
notably check read-pairing, repair read-pairing, and other stuff like trim and filter reads. 
Notably, `fq-repair` is the only tool (to my knowledge) 
that can successfully re-pair reads from gzipped FASTQ input.


## Installation and tests

To install as a python package (can also just be run as-is after cloning this repository): `pip install .`  

To run tests: `pytest`


## Current scripts

Run `commandname --help` for individual usage instructions.
Sample commands can also be found in the `tests/` directory.

**fq-repair** - Re-pair the reads in two FASTQ files if reads have been filtered out or otherwise reordered. 

**fq-checkpair** - Check if two FASTQ files are properly paired and highlight errors.

**fq-zwc** - Just a wrapper around `wc -l` for gzipped files.

**fq-filter** - Remove all reads in a FASTQ file below a certain Phred quality score. 

**fq-lenfilter** - Remove reads above or below a certain length.

**fq-trimmer** - Starting from both ends, trim a read so that bases below a certain Phred quality score are removed. If the entire read sucks (and there's not a single base above the minimum q score), the entire read is removed.

