# COGNICEPT SHELL #

This is a shell utility to configure Cognicept tools.

## Installation

### Dependencies

You need:

* Python 3
* Python 3 PIP

Install:

```
sudo apt-get install python3 python3-pip
```

### Package installation

To install the package locally, run:

```
pip3 install -e <path-to-the-repo>
```

To install from Python Package Index (PyPI), run:

```
pip3 install -i https://test.pypi.org/simple/ cognicept-shell==0.0.3
```

To verify installation, try to run

```
cognicept -h
```

If you get `cognicept: command not found` error, make sure that `~/.local/bin/` is in your `$PATH`. You could run this:

```
export PATH=$PATH:/home/$USER/.local/bin/
```
and add it to your `.bashrc` file.

## Tests

`cognicept-shell` is using `pytest` as the test framework. Make sure you install manually:

```
pip3 install pytest pytest-cov cli_test_helpers
```

To run tests, execute:

```
pytest --cov=cogniceptshell tests
```

To run ECR integration test, AWS credentials `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` with ECR access needs to be specified as environmental variables. If they are not specified, tests won't run.

## Running

### Configure

This feature allows you to configure Cognicept Tools. Run:

```
cognicept configure
```

The tool will let you change values of Cognicept Envrionmental variables.

## Building

To build the PyPI package, run:

```
python3 setup.py sdist bdist_wheel
```

Output will be lots of text, this command generates the build files. To upload the package, run:

```
python3 -m twine upload --repository testpypi dist/* --verbose
```

## Version history

* 0.0 [10/6/2020]
