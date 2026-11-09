name: Build Android APK

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Install dependencies
      run: |
        sudo apt update
        sudo apt install -y build-essential libffi-dev libssl-dev gettext libtool m4 autoconf
        pip3 install buildozer cython

    - name: Build APK with Buildozer
      run: buildozer android debug

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: PixelGlitch-APK
        path: bin/*.apk
