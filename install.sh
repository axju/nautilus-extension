#!/bin/sh
# install my nautilus extension directly from Github

echo "Create an extension directory"
mkdir -p ~/.local/share/nautilus/scripts
cd ~/.local/share/nautilus/scripts

echo "Download script"
curl -s https://raw.githubusercontent.com/axju/nautilus-extension/main/src/rename.py --output rename.py
chmod +x ~/.local/share/nautilus/scripts/rename.py

echo "Now the extension is ready. Have fun ;-)"
