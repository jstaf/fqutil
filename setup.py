import glob
from setuptools import setup

setup(
        name='fqutil',
        version='1.1',
        description='Several useful tools for manipulating FASTQ files.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/jstaf/fqutil',
        author='Jeff Stafford',
        author_email='jeff.stafford@queensu.ca',
        license='BSD-3',
        packages=['fqutil'],
        scripts=glob.glob('./fq-*'),
        zip_safe=False,
        setup_requires=['pytest-runner'],
        tests_require=['pytest']
        )
