"""Just some helper util functions"""

import re

def prefix_extension(filename, prefix):
    match = re.findall(r'(\.\w+(\.gz)?)$', filename)[0][0]
    return re.sub(match, prefix + match, filename)
