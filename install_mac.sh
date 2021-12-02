#!/bin/bash

# Check and install brew

if (which -s brew)
then
    echo 'Brew already installed'
else
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && echo 'Brew installed'
fi

# Install required system packages
brew install python3 tcl-tk python-tk zbar
brew upgrade

# Install required python packages to local environment
BREW_PYTHON=$(brew --prefix python3)/bin/python3

$BREW_PYTHON -m ensurepip --upgrade
rm -rf venv
mkdir venv
$BREW_PYTHON -m venv venv
./venv/bin/python3 -m pip install -r requirements.txt

