from setuptools import setup, find_packages
from codecs import open
import os

import modelmanager


def package_files(dir):
    return [os.path.join(p, f) for (p, d, n) in os.walk(dir) for f in n]


__version__ = modelmanager.__version__

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='model-manager',
    version=__version__,
    description='A python package to manage your (scientific) model runs, input and output.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jeffmaxey/modelmanager',
    download_url='https://github.com/jeffmaxey/modelmanager/tarball/' + __version__,
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 2.7',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    data_files=package_files('modelmanager/resources'),
    scripts=['modelmanager/scripts/modelmanager', 'modelmanager/scripts/mm'],
    include_package_data=True,
    author='Jeff Maxey',
    author_email='jeffmaxey@comcast.net'
)
