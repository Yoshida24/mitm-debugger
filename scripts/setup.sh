#!/bin/bash
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
echo '.env is created. please set env.'
