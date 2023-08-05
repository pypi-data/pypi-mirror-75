"""Uncertainty Baselines.

See more details in the
[`README.md`](https://github.com/google/uncertainty-baselines).
"""

import os
import sys

from setuptools import find_packages
from setuptools import setup

# To enable importing version.py directly, we add its path to sys.path.
version_path = os.path.join(os.path.dirname(__file__), 'uncertainty_baselines')
sys.path.append(version_path)
from version import __version__  # pylint: disable=g-import-not-at-top

setup(
    name='uncertainty_baselines',
    version=__version__,
    description='Uncertainty Baselines',
    author='Uncertainty Baselines Team',
    author_email='znado@google.com',
    url='http://github.com/google/uncertainty-baselines',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'absl-py>=0.5.0',
        'numpy>=1.7',
        'tf-nightly',
        'tensorflow-datasets>=1.3.0',
        'tf-models-nightly',  # Needed for BERT, depends on tf-nightly.
    ],
    extras_require={
        'tests': ['pylint>=1.9.0'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='probabilistic programming tensorflow machine learning',
)
