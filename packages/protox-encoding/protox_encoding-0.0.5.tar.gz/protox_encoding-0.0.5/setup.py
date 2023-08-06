import os
from distutils.core import Extension, setup

use_cython = bool(
    os.environ.get('USE_CYTHON', '').strip()
)

if use_cython:
    from Cython.Build import cythonize

if use_cython:
    ext = 'pyx'
else:
    ext = 'c'

extension = Extension(
    name='protox_encoding',
    sources=['protox_encoding.' + ext]
)

if use_cython:
    ext_modules = cythonize(extension)
else:
    ext_modules = [extension]

setup(
    name='protox_encoding',
    version='0.0.5',
    ext_modules=ext_modules
)
