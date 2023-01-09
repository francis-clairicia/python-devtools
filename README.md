# python-devtools
Common utilities for python projects powered by pip's requirements.txt workflow

## Installation
```
git submodule add https://github.com/francis-clairicia/python-devtools.git devtools
```

Optionally, configure the local .git to always fetch submodules information:
```
git config submodule.recurse true
```

## Usage
```
python -m devtools --help
```

### Configuration
The `devtools` package will read a `.devtools.cfg` file located at your current working directory to extend the actual configuration
```ini
[devtools:file:requirements.txt]
input = pyproject.toml
; extras = test, doc
; all-extras = true (if true, 'extras' option is ignored)

[devtools:file:requirements-dev.txt]
input = requirements/requirements-dev.in

[devtools:file:requirements-test.txt]
input = requirements/requirements-test.in

```
