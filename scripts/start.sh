#!/bin/bash
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/bot
python bot/main.py
