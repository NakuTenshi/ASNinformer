#!/usr/bin/env bash



file='./ASNinformer.py'
name="$(basename "${file%.py}")"

## Requirements
pip3 install -r requirements.txt

cp -r "$file" "$HOME/.local/bin/$name"
echo "Done."
