#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
sbmlsim pip package
"""
import io
import re
import os
from setuptools import find_packages
from setuptools import setup

setup_kwargs = {}


def read(*names, **kwargs):
    """ Read file info in correct encoding. """
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


# version from file
verstrline = read('sbmlsim/_version.py')
mo = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", verstrline, re.M)
if mo:
    verstr = mo.group(1)
    setup_kwargs['version'] = verstr
else:
    raise RuntimeError("Unable to find version string")

# description from markdown
long_description = read('README.rst')
setup_kwargs['long_description'] = long_description

# ray not supported on windows
if os.name == 'nt':
    install_ray = []
else:
    install_ray = [
        "ray>=0.8.6",
    ]

setup(
    name='sbmlsim',
    description='SBML simulation made easy',
    url='https://github.com/matthiaskoenig/sbmlsim',
    author='Matthias König',
    author_email='konigmatt@googlemail.com',
    license='LGPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Cython',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    keywords='SBML, simulation',
    packages=find_packages(),
    # package_dir={'': ''},
    package_data={
      '': [
              '../requirements.txt',
               'tests/data',
          ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
    # List run-time dependencies here.  These will be installed by pip when
    install_requires=[
        "pip>=19.3.1",
        "numpy>=1.19.0",
        "scipy>=1.5.1",
        "sympy>=1.6.1",
        "pandas>=1.0.5",
        "tables>=0.3.6",
        "xarray>=0.15.1",
        "bottleneck>=1.3.2",
        "pint>=0.14",

        "python-libsbml-experimental>=5.18.1",
        "python-libsedml>=2.0.11",
        "python-libcombine>=0.2.7",
        "python-libnuml>=1.1.1",
        "libroadrunner>=2.0.0",

        "psutil>=5.6.3",
        "setproctitle>=1.1.10",

        "matplotlib>=3.3.0",
        "plotly",
        "altair>=4.0.0",
        "seaborn>=0.10.0",

        "coloredlogs",
        "pyDOE>=0.3.8",

        "Sphinx",
        "sphinx_rtd_theme",
        "recommonmark",

    ] + install_ray,
    extras_require={},
    **setup_kwargs)
