
import pkgutil
import os

THEME_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)))
THEMES = {}

for importer, name, _ in pkgutil.iter_modules([THEME_PATH]):
    module = importer.find_module(name).load_module(name)
    THEMES[module.__name__] = module.COLORS
