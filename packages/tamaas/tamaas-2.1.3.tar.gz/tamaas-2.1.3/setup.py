import setuptools
import shutil
import sysconfig
import os

long_description = """
# Tamaas — A fast rough contact library

[![status](https://joss.theoj.org/papers/86903c51f3c66964eef7776d8aeaf17d/status.svg)](https://joss.theoj.org/papers/86903c51f3c66964eef7776d8aeaf17d)

Tamaas (from تماس meaning “contact” in Arabic and Farsi) is a
high-performance rough-surface periodic contact code based on boundary and
volume integral equations. The clever mathematical formulation of the underlying
numerical methods allows the use of the fast-Fourier Transform, a great help in
achieving peak performance: Tamaas is consistently two orders of magnitude
faster (and lighter) than traditional FEM! Tamaas is aimed at researchers and
practitioners wishing to compute realistic contact solutions for the study of
interface phenomena.

## Disclaimer

This package is intended for ease of installation for Linux platforms, but comes
with NO WARRANTY of compatibility. If you experience any issue, please install
Tamaas from [source](https://c4science.ch/source/tamaas/). We provide a Docker
image for non-Linux systems. This package contains unsigned binary blobs: if you
are concerned about security, please build Tamaas from source (the commits are
signed).

Tamaas is the result of a science research project. To give proper credit to
Tamaas and the researchers who have developed the numerical methods that it
implements, please cite the [JOSS
paper](https://joss.theoj.org/papers/86903c51f3c66964eef7776d8aeaf17d) and the
appropriate references therein.

## Dependencies

Essentials:

- FFTW with OpenMP support (needs to be installed separately,
  e.g. with your system's package manager)
- Numpy

Optional:

- Scipy (for non-linear solvers)
- UVW (for dumpers)
- h5py (for dumpers)
- netCDF4 (for dumpers)

To install with all dependencies (except FFTW), run ``pip install
tamaas[solvers,dumpers]``.

## Documentation

Documentation can be found on [tamaas.readthedocs.io](https://tamaas.readthedocs.io/en/latest/).
"""

version = "2.1.3"
major = version.split('.')[0]

if True:
    shutil.copyfile('../../README.md', 'README.md')
    shutil.copyfile('../src/libTamaas.so.{}'.format(version),
                    'tamaas/libTamaas.so.{}'.format(major))

setuptools.setup(
    name="tamaas",
    version="2.1.3",

    packages=setuptools.find_packages(),
    include_package_data=True,
    author=', '.join([u'Lucas Fr\xe9rot', 'Guillaume Anciaux', 'Valentine Rey', 'Son Pham-Ba', u'Jean-Fran\xe7ois Molinari']),
    author_email="lucas.frerot@protonmail.com",
    description='A fast library for periodic elastic '
    'and elasto-plastic rough contact',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://c4science.ch/project/view/2036/",
    install_requires=['numpy'],
    extras_require={
        "dumpers": ['uvw', 'h5py', 'netCDF4'],
        "solvers": ['scipy'],
    },
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
    ]
)
