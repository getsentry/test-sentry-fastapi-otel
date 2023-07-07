#!/usr/bin/env bash

set -euo pipefail


source .venv/bin/activate



printenv | grep SENTRY

python main.py "$@"
