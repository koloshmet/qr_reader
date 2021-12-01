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

# Install required python packages to local environment
/usr/local/bin/python3 -m ensurepip --upgrade
mkdir venv && /usr/local/bin/python3 -m venv venv
./venv/bin/python3 -m pip install -r requirements.txt

