#!/bin/bash
rm -r $(find . -name '*.egg-info')
rm -r $(find . -name '__pycache__')
rm -r $(find . -name '.pytest_cache')
rm -r .eggs/
rm -r build/
rm -r dist/