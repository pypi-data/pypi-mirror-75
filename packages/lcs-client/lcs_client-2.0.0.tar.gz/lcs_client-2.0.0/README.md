# python-lcs-client
A client for server side Python applications to interact with LCS, the HackRU backend.
The general idea is for this to be used with a JSON based web API.
For every request to your API, you would ask for a LCS token.

Alternatively you could have your own tokens, and have the user pass in
the password again but this will be annoying for the user if they already
logged into the HackRU frontend

## Documentation
 - [Documentation for this client](lcs_client.md)
 - [Documentation for LCS](https://github.com/hackru/lcs/wiki)

## Installation
```bash
pip install lcs_client
```

## Development setup
1. Create virtual environment locally
    ```bash
    virtualenv -p python3 env
    ```
    OR
    ```bash
    python3 -m venv env
    ```
1. Activate the virtual environment
    ```bash
    source env/bin/activate
    ```
1. Install the required dependencies (prod and dev) into the virtual environment
    ```bash
    pip install -e .[dev]
    ```

##### Installing lcs_client (after making local code changes)
Run the following in terminal:
```bash
pip install -e .
```
This will install the package as if you installed it from PyPi so that you can perform testing using the package 
rather than the local file
##### Running tests
Run the following command from terminal:
```bash
pytest
```

## Generating documentation
Pre-requisite: 
* [Perform Development setup](#Development setup)

Run the following from terminal (which will use the configuration within `pdoc-markdown.yml`):
```bash
pydoc-markdown
```
The generated documentation is within `lcs_client.md`  
Edit the README.md as required according to the changes made

## Running the example web application
```bash
pip install -r example_requirements.txt
python example_api.py
```

## Release on PyPi
Pre-requisites:
* [Perform Development setup](#Development setup)
* Ensure version changes are appropriately reflected using semantic versioning in `lcs_client/__init__.py` and 
`setup.py` (as well as any other source files)
* Ensure documentation is up to date by following the steps within [Generating documentation](#Generating documentation)
* Ensure code has been committed to the GitHub repo with a tag and commit message that include the version number
1. Install wheel to build and twine to upload package
    ```bash
    pip install -e .[build]
    ```
1. Build the source archive and wheel for package
    ```bash
    python setup.py sdist bdist_wheel
    ```
1. Examine the archive to ensure it includes the expected files
1. Check for common errors
    ```bash
    twine check dist/*
    ```
1. Upload to TestPyPi and ensure correctness
    ```bash
    twine upload --repository testpypi dist/*
    ```
    If it errors out about not having permissions to upload, simply change the name within setup.py and restart from step 2
1. Upload the new release
    ```bash
    twine upload dist/*
    ```
