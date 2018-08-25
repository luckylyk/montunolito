import sys
import os
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit'
    }
}

executable_path = (
    os.path.join(
        os.path.dirname(__file__),
        'applications',
        'montunomakina',
        '__main__.py'))

executables = [
    Executable(executable_path, base=base)
]

setup(name='MontunoMakina',
      version='0.1',
      description='Montuno Makina',
      options=options,
      executables=executables
)