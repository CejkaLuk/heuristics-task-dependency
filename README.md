# Heuristic Methods for Activity Dependency Problems (HMADP)
Project comparing heuristic methods on activity-dependency problems. Implementation
was done using Python for the _Heuristic Algorithms_ course at FNSPE CTU.

## Dependencies

### Core Dependencies

The core dependencies for the HMADP project are:

* [Python](https://www.python.org/>) - version 3.9.6 or newer.

### Python Package Dependencies

The dependencies for HMADP are the following Python packages:

* [matplotlib](https://matplotlib.org/stable/) - for visualizing problem timelines
* [nose2](https://docs.nose2.io/en/latest/>) - for unit tests
* [nose2-cov](https://pypi.org/project/nose2-cov/>) - for test coverage (with
  reports etc.)
* [numpy](https://numpy.org/) - for various operations during visualization
* [sphinx](https://www.sphinx-doc.org/en/master/>) - for generating the
  documentation

They can be installed using the `init` task predefined in `Makefile`:

```
$ make init
```

## How To

### Run Unit Tests

Unit tests are written using the [nose2](https://docs.nose2.io/en/latest/>)
testing framework. They can be run using the following tasks predefined in
`Makefile`:

```bash
# Run tests only
$ make tests

# Run tests with coverage
$ make tests_coverage

# Run tests with coverage and output the results into a html report
$ make tests_coverage_report
```

To remove the generated coverage report run:

```
$ make clean
```

### Build the Documentation

Documentation is generated using
[sphinx](https://www.sphinx-doc.org/en/master/>). To build the documentation go
to `docs/` and run the following predefined task:

```
$ make html
```

To remove the documentation generate in `docs/build/` execute the following in `docs/`:
```
$ make clean
```

## Development

### Visual Studio Code
The project was developed using Visual Studio Code. In an effort to produce
conventional and somewhat correct code, a selection of Visual Studio Code
extensions and non-default settings were employed.

#### Extensions
- [Pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint)
   \- Linting of Python code
- [Rewrap](https://marketplace.visualstudio.com/items?itemName=stkb.rewrap) \-
   Word wrapping

#### Non-default VS Code Settings
- `Files: Trim Trailing Whitespace` - Trim the trailing whitespace at the end of a
  line when saving a file.
