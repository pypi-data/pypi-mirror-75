# Relevance.io Python Libraries

This package contains the libraries that allows other applications to easily integrate
with the Relevance.io APIs.

## Getting started

### Requirements

These are the general requirements for using this package:

- Python 3.6 or higher
- Other things, depending on the specific library used...

### Installation

Since this is a standard Python package, install with:

    pip install .

Note that this package does not include any classifiers. They must be installed separately.

#### Development mode

Again, as this is a standard Python package, install in development (editable) mode with:

    pip install -e .

## Building

The Python artifacts can be build using the standard `setup.py` script:

    ./setup.py sdist
    ./setup.py bdist_egg
    ./setup.py bdist_wheel

...to build a source distribution, a binary egg distribution and a wheel distribution, respectively.

## Documentation

The code documentation is placed in the `docs/` directory. To generate it, first, generate
the API documentation from the code using a custom `setup.py` command:

    ./setup.py build_apidoc

Then, generate the complete documentation using Sphinx:

    ./setup.py build_sphinx

This will generate the documentation files in the `build/docs/` directory.

## Testing

The `setup.py` script provides commands to test the code before distributing it. Run
them with:

    ./setup.py test         # runs the tests/ directory
    ./setup.py lint         # validates code syntax

## License

This code and its documentation is provided under the MIT License, bundled as the `LICENSE`
file. All original rights are reserved to Relevance.io 2020-.
