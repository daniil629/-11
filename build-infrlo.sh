#!/bin/sh
set -eu

cd "$(dirname "$0")"
python3 -m pip install --disable-pip-version-check --no-cache-dir -r requirements.txt
