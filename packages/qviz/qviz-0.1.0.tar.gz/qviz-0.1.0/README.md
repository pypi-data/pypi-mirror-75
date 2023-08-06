
# qviz

[![Build Status](https://travis-ci.org/Qbeast/qviz.svg?branch=master)](https://travis-ci.org/Qbeast/qviz)
[![codecov](https://codecov.io/gh/qbeast_io/qviz/branch/master/graph/badge.svg)](https://codecov.io/gh/Qbeast/qviz)


Qbeast's Jupyterlab widgets

## Installation

You can install using `pip`:

```bash
pip install qviz
```

Or if you use jupyterlab:

```bash
pip install .
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-materialui  
jupyter labextension install ipysheet
jupyter labextension install .
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash

jupyter nbextension enable --py [--sys-prefix|--user|--system] qviz
```

## Voila
To use with Voila you must install
```bash
jupyter nbextension install voila --sys-prefix --py
jupyter nbextension enable voila --sys-prefix --py
```
## Development
The structure of this repository comes from https://github.com/jupyter-widgets/widget-ts-cookiecutter.


#Testing
To run all tests
```bash 
py.test
npm tests

# To run test by hand, install those global dependencies
sudo npm install --global  karma-mocha karma-mocha-reporter karma-typescript karma-typescript-es6-transform typescript acorn karma-script-launcher mocha
pip install pytests nbval

``` 
## Development
``bash

pip install -e .
jupyter nbextension install --py --symlink --sys-prefix qviz
jupyter nbextension enable --py --sys-prefix qviz
jupyter labextension link .

``