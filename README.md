# fqutils

A couple Python-based FASTQ QC tools that perform common operations like trimming poor quality bases calls from reads, filtering out bad reads, and re-pair paired-end reads after QC (when bad reads/adapters get filtered out by QC, the reads that no longer have a pair need to be separated out). 

Requires Python 3.4, but otherwise can be invoked from the command-line like any other program. You can install this package using `pip`: `pip install .`. To run tests: `pytest`

==============================================

**fq-repair** - Re-pair the reads in two FASTQ files if reads have been filtered out or otherwise reordered. It's basically a Python version of [cmpfastq.pl](http://compbio.brc.iop.kcl.ac.uk/software/cmpfastq.php), except that it actually works with the latest Illumina format and can handle gzipped files.
  
This creates four output files:
  +  fastq1_common.fastq[.gz] - reads that were present in both files (and in the correct order too!)
  +  fastq1_unique.fastq[.gz] - reads present only in fastq1
  +  fastq2_common.fastq[.gz] - reads that were present in both files
  +  fastq2_unique.fastq[.gz] - reads present only in fastq2
  
The unique reads can be aligned as single-end reads depending on your aligner.

==============================================

**fq-filter** - Remove all reads in a FASTQ file below a certain Phred quality score. 

  Usage: fq-filter [-q \<minReadQual\>] [-o \<outputfile\>] \<inputFile\>
  
  Default value for -q is 30. Output is to console unless you specify a value for -o
  
===========================================  
  
**fq-trimmer** - Starting from both ends, trim a read so that bases below a certain Phred quality score are removed. If the entire read sucks (and there's not a single base above the minimum q score), the entire read is removed.

  Usage: fq-trimmer [-q \<minReadQual\>] [-o \<outputfile\>] \<inputFile\>  
  
  Default value for -q is 30. Output is to console unless you specify a value for -o
