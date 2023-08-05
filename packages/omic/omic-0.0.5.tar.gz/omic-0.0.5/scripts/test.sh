#!/bin/bash
# 
# Run tests on Omic client
if ! [ -x "$(command -v pytest)" ]; then
    echo 'Error: Python module "pytest" is not installed.' >&2
    exit 1
fi
./scripts/clean.sh
python3 setup.py develop -u
python3 -m pip install --editable .
pytest -p no:warnings -s
exit $?