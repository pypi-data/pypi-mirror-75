# Adapted from Tensorflow under http://www.apache.org/licenses/LICENSE-2.0
"""PD3 is a modern, accelerated library for discrete dislocation dynamics.

This release contains only stub code for a dependent project.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fnmatch
import os
import re
import sys

from glob import glob

from setuptools import Command
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install as InstallCommandBase
from setuptools.dist import Distribution

# This version string is semver compatible, but incompatible with pip.
# For pip, we will remove all '-' characters from this string, and use the
# result for pip.
_VERSION = '0.0.1'

REQUIRED_PACKAGES = [
    'absl-py >= 0.7.0',
    'numpy >= 1.16.0, < 2.0',
    'protobuf >= 3.9.2',
    'wheel >= 0.26',
    'six >= 1.12.0',
    'typing-extensions >= 3.7.4',
    # scipy < 1.4.1 causes segfaults due to pybind11
    'scipy == 1.4.1',
]

project_name = 'pd3'
if '--project_name' in sys.argv:
    project_name_idx = sys.argv.index('--project_name')
    project_name = sys.argv[project_name_idx + 1]
    sys.argv.remove('--project_name')
    sys.argv.pop(project_name_idx)

DOCLINES = __doc__.split('\n')


class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True



def find_files(pattern, root):
    """Return all the files matching pattern below root dir."""
    for dirpath, _, files in os.walk(root):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(dirpath, filename)


so_lib_paths = [
    i for i in os.listdir('.')
    if os.path.isdir(i) and fnmatch.fnmatch(i, '_solib_*')
]

matches = []
for path in so_lib_paths:
    print(path)
    matches.extend(
        ['../' + x for x in find_files('*', path) if '.py' not in x])

licenses = glob("pd3/licenses/*")

headers = (list(find_files('*.proto', 'pd3/proto')) +
           list(find_files('*.h', 'pd3/cc/includes')))

setup(
    name=project_name,
    version=_VERSION.replace('-', ''),
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    url='https://github.com/dmadisetti/pd3/',
    download_url='https://github.com/dmadisetti/pd3/tags',
    author='Dylan Madisetti',
    author_email='madisetti@jhu.edu',
    # Contained modules and scripts.
    packages=['pd3'],
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES,
    # Add in any packaged data, but not that this is not bound to be respected
    # by bdist_wheel
    include_package_data=True,
    # PyPI package information.
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
    ],
    license='MIT',
    license_files=licenses,
    keywords='pd3 discrete dislocation dynamics ddd',
)
