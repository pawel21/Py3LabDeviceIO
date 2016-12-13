#!/usr/bin/env bash
if [[ `uname` == 'Linux' ]]; then
    if ! [[ -x "$(command -v pip)" ]]; then
        sudo apt-get install -y python-pip
    fi
else
    echo "This script is only supported on Ubuntu"
    exit 1
fi

pip3 install virtualenv

virtualenv -p python3 venvenv
pip3 install --upgrade virtualenv
source venvenv/bin/activate
python -m pip install -r requirements.txt
deactivate
