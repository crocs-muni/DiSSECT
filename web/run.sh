#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=development
sage --python -m flask run --no-reload
