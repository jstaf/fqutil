# fastqUtils

A couple Python-based FASTQ QC tools that perform common operations like trimming poor quality bases calls from reads, filtering out bad reads, and re-pair paired-end reads after QC (when bad reads/adapters get filtered out by QC, the reads that no longer have a pair need to be separated out). These tools auto-detect the Phred/Illumina format, so you don't need to worry about issues in that regard.

Requires Python 3.4, but otherwise can be invoked from the command-line like any other program.

==============================================

**FASTQFilter.py** - Remove all reads in a FASTQ file below a certain Phred quality score. 

  Usage: ./FASTQFilter.py [-q <minReadQual>] [-o <outputfile>] <inputFile>
  
  Default value for -q is 30. Output is to console unless you specify a value for -o
  
===========================================  
  
**FASTQTrimmer.py** - Starting from both ends, trim a read so that bases below a certain Phred quality score are removed. If the entire read sucks (and there's not a single base above the minimum q score), the entire read is removed.

  Usage: ./FASTQTrimmer.py [-q <minReadQual>] [-o <outputfile>] <inputFile>  
  
  Default value for -q is 30. Output is to console unless you specify a value for -o

============================================  
  
**matchFASTQ.py** - Re-pair the reads in two FASTQ files if reads have been filtered out or otherwise reordered. It's basically a Python version of [cmpfastq.pl](http://compbio.brc.iop.kcl.ac.uk/software/cmpfastq.php), except that it actually works with the latest Illumina format (cmpfastq is currently bugged and outputs everything as "unique").

  Usage: ./matchFASTQ.py [-r] -1 <FASTQfile1> -2 <FASTQfile2>
  
  -r controls what Python regular expression is used to parse the Illumina headers (you can change it if your reads have a funky header ID). The default for -r is currently '\w+:\w+\s', which corresponds to the X/Y read coordinate position in the tile.
  
This creates four output files:
  +  FASTQfile1.common - reads that were present in both files (and in the correct order too!)
  +  FASTQfile1.unique - reads present only in FASTQfile1
  +  FASTQfile2.common - reads that were present in both files
  +  FASTQfile2.unique - reads present only in FASTQfile2
  
The unique reads can be aligned as single end reads when using an aligner like TopHat2.
