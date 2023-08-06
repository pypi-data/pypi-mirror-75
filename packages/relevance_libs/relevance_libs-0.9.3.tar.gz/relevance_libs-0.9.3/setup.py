#!/usr/bin/python3

# pylint: disable=missing-docstring,import-error,multiple-imports

import distutils
import distutils_cmd
from setuptools import setup
from setuptools import find_packages

import relevance_libs as main


setup(
    name=main.__name__,
    version=main.__version__,

    description=main.__doc__.split('\n')[1].strip(),
    long_description=main.__doc__.strip(),
    url='http://www.relevance.io',
    author='Relevance.io',
    author_email='info@relevance.io',
    maintainer=main.__author__,
    maintainer_email=main.__author_email__,

    license=main.__license__,
    platforms=['any'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=find_packages(exclude=['tests', 'tests.*']),
    provides=[main.__name__],

    cmdclass={
        'clean': distutils_cmd.CleanCommand,
        'build_apidoc': distutils_cmd.BuildApidocCommand,
        'build_sphinx': distutils_cmd.BuildSphinxCommand,
        'lint': distutils_cmd.LintCommand,
    },

    python_requires='>=3.6',
    setup_requires=[
        'Sphinx>=3.0.3',
        'pylint>=2.5.2',
    ],

    tests_require=[],
    test_suite='tests',

    install_requires=list(open('requirements.txt')),
)
