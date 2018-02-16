import glob
from setuptools import setup

setup(
        name='fqutil',
        version='1.0',
        description='Several useful tools for manipulating FASTQ files.',
        url='https://github.com/jstaf/fqutil',
        author='Jeff Stafford',
        license='BSD-3',
        packages=['fqutil'],
        scripts=glob.glob('./fq-*'),
        zip_safe=False,
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
        )
