
import codecs
import os

import setuptools
from setuptools import setup

# Save version and author to __meta__.py
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'auto-cmdline', '__meta__.py')
meta = '''# Automatically created. Please do not edit.
__version__ = '%s'
__author__ = 'jarndt'
''' % version
with open(path, 'w') as F:
    F.write(meta)

setup(
    # Basic info
    name='auto-cmdline',
    version=version,
    author='jarndt',
    author_email='unsupo@gmail.com',
    url='',
    description='Auto generate commandline for any python script',
    long_description=codecs.open('README.md', 'rb', 'utf8').read(),
    long_description_content_type="text/markdown",

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],
    license="MIT",

    # Packages and dependencies
    # package_dir={'': 'auto-cmdline'},
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'auto-cmdline[dev]',
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)