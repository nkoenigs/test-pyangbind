#!/usr/bin/env bash
pip uninstall -y pyangbind
pip install -r requirements.txt
python3 test_pyangbind.py