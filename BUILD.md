# Build MacOS app

### 1. Install libraries with brew
* zbar
* tcl-tk
* python-tk
* python3

### 2. Install pip, venv and python requirements:
```
python3 -m ensurepip --upgrade
mkdir venv && python3 -m venv venv
./venv/bin/python3 -m pip install -r requirements.txt
```

### 3. Install pyinstaller

`./venv/bin/python3 -m pip install pyinstaller`

### 4. Build app

`./venv/bin/pyinstaller main.py -n 'HSE Party Qr Reader' -w --noconfirm --clean --paths="/usr/local/lib/python3.9/site-packages/cv2/" `

### 5. Change app properties

Add to `./dist/HSE Party Qr Reader.app/Contents/Info.plist`

```
<key>NSCameraUsageDescription</key>
<string>Please</string>
```