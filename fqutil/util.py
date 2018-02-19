'''
Some helper util functions
'''

import re

def prefix_extension(filename, prefix):
    match = re.findall(r'(\.\w+(\.gz)?)$', filename)[0][0]
    return re.sub(match, prefix + match, filename)


def is_gzip(filename):
    return len(re.findall(r'.gz$', filename)) > 0
