#!/bin/bash

version=0.0.1
bin=oxag-$version-`uname -s`-`uname -m`

rm -rf *.spec build dist __pycache__
python -O -m PyInstaller --onefile oxag.py
cd dist
mv oxag $bin
