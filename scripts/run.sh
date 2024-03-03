#!/bin/bash
. .venv/bin/activate
set -a && . ./.env && set +a
mitmweb
