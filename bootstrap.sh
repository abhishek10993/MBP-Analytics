#!/bin/bash
export FLASK_APP=./REST_Controllers/index.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0
