#!/usr/bin/env bash

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

file='./ASNinformer.py'
name="$(basename "${file%.py}")"

## Requirements
python3 -m pip3 install rich

cp -r $file /bin/$name
echo "Done."
