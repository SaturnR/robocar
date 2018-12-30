#!/usr/bin/env bash

export FLASK_APP=api.py
flask run -p 8080 -h 0.0.0.0 --cert cert.crt --key cert.key 

