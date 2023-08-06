# Group 4

## Common Utils package

## Common Utils Package
#### Dependencies
Python packages to build: `setuptools` and `wheel`  
Python packages to deploy: `twine`  
To install: `python3 -m pip install --upgrade setuptools wheel twine`

#### Building & deploy the package
1. `cd common-utils`
1. `python3 setup.py sdist bdist_wheel`
1. `python3 -m twine upload dist/*`