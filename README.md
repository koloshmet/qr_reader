# Qr reader for party

## How to install

### Common steps

#### 1. Download archive from here

#### 2. Unpack it

#### 3. Open terminal

#### 4. Go to the folder where the files were unpacked
Example: `cd ~/Downloads/qr_reader`

### Simple way
#### 5. Run install script for your OS
MacOS: `./install_mac.sh`

Linux: `./install_linux.sh`

### Difficult way
#### 5. Install with your package manager e.g. brew (MacOS) or apt (Linux) following packages:
* libzbar0 (Linux)
* libzbar-dev (Linux)
* python3-tk (Linux)
* python3-pip (Linux)
* python3 (MacOS)
* zbar (MacOS)
* tcl-tk (MacOS)
* python-tk (MacOS)

It has to look like:

`brew install python3` (MacOS)

`sudo apt install python3-pip` (Linux)

#### 6. Install python libraries:
```
python3 -m ensurepip --upgrade
mkdir venv && python3 -m venv venv
./venv/bin/python3 -m pip install -r requirements.txt
```

## How to use
Run **run.sh**:

`./run.sh`

If you do everything right, it starts immediately
