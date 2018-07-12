# every pattern contains 5 keys: 1, 2, 3, 4, relationships
# keys 1, 2, 3, 4 contains differents alternative array of hand pattern index.
# the key number correspond the quarter of the pattern (1 = first quarter, etc)
# the 'relationship' key contains a dict. His keys represent the pattern index
# it contain the pattern index of the next quarter and a value
# (between 0 and 5)
# it's for generate random patterns.
# this is data and will be moved in JSON files. Every pattern will be save as
# different json file.

import pkgutil
import os

PATTERN_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'datas')
PATTERNS = {}

for importer, name, _ in pkgutil.iter_modules([PATTERN_PATH]):
    module = importer.find_module(name).load_module(name)
    PATTERNS[module.NAME] = module.PATTERN
