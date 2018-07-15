
import pkgutil
import os

PATTERN_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)))
PATTERNS = {}

for importer, name, _ in pkgutil.iter_modules([PATTERN_PATH]):
    module = importer.find_module(name).load_module(name)
    PATTERNS[module.NAME] = module.PATTERN
