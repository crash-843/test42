#!/bin/bash

filename="logs/$(date +%Y-%m-%d).dat"
python manage.py get_models 2> $filename