#!/usr/bin/env bash

set -euo pipefail

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

printenv | grep SENTRY

uvicorn microservice:app --port 5001 --reload