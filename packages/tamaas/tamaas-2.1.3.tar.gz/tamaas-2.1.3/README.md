Tamaas --- A blazingly fast rough contact library
=================================================

Tamaas is a C++/Python library that implements a number of numerical methods
based on integral equations to efficiently solve contact problems with rough
surfaces. The word تماس (tamaas) means "contact" in Arabic and Farsi.

## Quick Start

If you have a Linux system with Python 3.7+ installed, you can simply run `pip3
install tamaas`. Note however that there may be incompatibilities between Linux
distributions (the PyPI package was built on Debian Buster), so if you encounter
an issue, please compile from source.

## Dependencies

Here is a list of dependencies to compile Tamaas:

- a //C++ compiler// with full //C++14// and //OpenMP// support
- [SCons](https://scons.org/) (python build system)
- [FFTW3](http://www.fftw.org/) compiled with //OpenMP// support
- [boost](https://www.boost.org/) (preprocessor)
- [thrust](https://github.com/thrust/thrust) (1.9.2+)
- [python 3+](https://www.python.org/) (probably works with python 2, but it
  is not tested) with [numpy](https://numpy.org/)
- [pybind11](https://github.com/pybind/pybind11) (included as submodule)
- [expolit](https://c4science.ch/source/expolit/) (included as submodule)

Optional dependencies are:

- [scipy](https://scipy.org) (for nonlinear solvers)
- [uvw](https://pypi.org/project/uvw/) (for dumpers)
- [googletest](https://github.com/google/googletest) and
  [pytest](https://docs.pytest.org/en/latest/) (for tests)
- [Doxygen](http://doxygen.nl/) and
  [Sphinx](https://www.sphinx-doc.org/en/stable/) (for documentation)

Note that a Debian distribution should have the right packages for all these
dependencies (they package the right version of thrust extracted from CUDA in
`stretch-backports non-free` and `buster non-free`).

## Compiling

You should first clone the git submodules that are dependencies to tamaas
(expolit, pybind11 and googletest):

    git submodule update --init --recursive

The build system uses SCons. In order to compile Tamaas with the default
options:

    scons

After compiling a first time, you can edit the compilation options in the file
`build-setup.conf`, or alternatively supply the options directly in the command
line:

    scons option=value [...]

To get a list of //all// build options and their possible values, you can run
`scons -h`. You can run `scons -H` to see the SCons-specific options (among them
`-j n` executes the build with `n` threads and `-c` cleans the build). Note that
the build is aware of the `CXX` and `CXXFLAGS` environment variables.

## Installing

Before you can import tamaas in python, you need to install the python package
in some way.

### Using pip

You have two choices to install tamaas:

- An out-of-repository installation to a given prefix (e.g. `/usr/local`, or a
  python virtual environment)
- A development installation to `~/.local` which links to the build directory

The former is simply achieved with:

    scons prefix=/your/prefix install

    # Equivalent to (if you build in release)
    install build-release/src/libTamaas.so* /your/prefix/lib
    pip3 install --prefix /your/prefix build-release/python

The compiled parts of the python module should automatically know where to find
the Tamaas shared library, so no need to tinker with `LD_LIBRARY_PATH`. The
second installation choice is equally simple:

    scons dev

    # Equivalent to
    pip3 install --user -e build-release/python

You can check that everything is working fine with:

    python3 -c 'import tamaas; print(tamaas)'

### Using environment variables (not recommended)

You can source (e.g. in your `~/.bashrc` file) the file
`build-release/tamaas_environment.sh` to modify the `PYTHONPATH` and
`LD_LIBRARY_PATH` environment variables. This is however not recommended because
these variables may conflict in a python virtual environment (i.e. if you use
`virtualenv` with tamaas).

## Tests

To run tests, make sure to have [pytest](https://docs.pytest.org/en/latest/)
installed and run `scons test` if you have compiled Tamaas with tests activated
(`scons build_tests=True use_googletest=True`).

## Documentation

The latest documentation is available on
[ReadTheDocs](https://tamaas.readthedocs.io/en/latest/)! Note however that due
to technical limitations, the Python API documentation is not available online.
You'll need to compile the documentation locally.

To build the documentation, activate the `build_doc` option and run `scons doc`.
Make sure you have
[sphinx-rtd-theme](https://pypi.org/project/sphinx-rtd-theme/) and
[breath](https://pypi.org/project/breathe/) installed. The compiled indexes for
the doxygen C++ API and Sphinx documentation can be found in
`doc/build/{doxygen,sphinx}/html/index.html`. Beware however that manually
compiling documentation leads to a lot of warnings.

## Examples

Example simulations can be found in the `examples/` directory. There is no
guarantee that the examples in `examples/legacy/` all work however.

- `rough_contact.py` shows a typical normal rough contact simulation
- `adhesion.py` shows how you can derive some classes from Tamaas in python,
  here to implement a custom adhesion potential
- `plasticity.py` computes an elastoplastic Hertz simulation and dumps the
  result in `examples/paraview/` in VTK format
- `stresses.py` shows how you can compute stresses from a boundary traction
  distribution
- the scripts in `pipe_tools` allow to execute elastic contact simulations
  without the need to code a custom script (see documentation for more details)

## Contributing

Contributions to Tamaas are welcome! Please follow the guidelines below.

### Report an issue

If you have an account on [c4science](https://c4science.ch), you can [submit an
issue](https://c4science.ch/maniphest/task/edit/?owner=frerot&projectPHIDs=tamaas&view=public).
All open issues are visible on the
[workboard](https://c4science.ch/project/board/2036/), and the full list of
issues is available [here](https://c4science.ch/maniphest/query/1jDBkIDDxCAP/).

### Submit a patch / pull-request

C4Science runs [Phabricator](https://www.phacility.com/phabricator/) to host the
code. The procedure to submit changes to repositories is described in this
[guide](https://secure.phabricator.com/book/phabricator/article/arcanist_diff/).
In a nutshell:

```lang=bash
# Make changes
git commit           # Any number of times
arc diff             # Pushes all new commits for review
# Wait for review...
```

## Citing

Tamaas is the result of a science research project. To give proper credit to
Tamaas and the researchers who have developed the numerical methods that it
implements, please cite Tamaas as:

Frérot , L., Anciaux, G., Rey, V., Pham-Ba, S., & Molinari, J.-F. Tamaas: a
library for elastic-plastic contact of periodic rough surfaces. Journal of Open
Source Software, 5(51), 2121 (2020).
[doi:10.21105/joss.02121](https://doi.org/10.21105/joss.02121)

If you use the elastic-plastic contact capabilities of Tamaas, please cite:

Frérot, L., Bonnet, M., Molinari, J.-F. & Anciaux, G. A Fourier-accelerated
volume integral method for elastoplastic contact. Computer Methods in Applied
Mechanics and Engineering 351, 951–976 (2019)
[doi:10.1016/j.cma.2019.04.006](https://doi.org/10.1016/j.cma.2019.04.006).

If you use the adhesive contact capabilities of Tamaas, please cite:

Rey, V., Anciaux, G. & Molinari, J.-F. Normal adhesive contact on rough
surfaces: efficient algorithm for FFT-based BEM resolution. Comput Mech 1–13
(2017)
[doi:10.1007/s00466-017-1392-5](https://doi.org/10.1007/s00466-017-1392-5).


## License

Tamaas is distributed under the terms of the [GNU Affero General Public License
v3.0](https://www.gnu.org/licenses/agpl.html).
