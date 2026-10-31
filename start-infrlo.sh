#!/bin/sh
set -eu

cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1
exec python3 -m app.main
