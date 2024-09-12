#!/bin/bash
cd $( dirname $0 )
cd ../

export DJANGO_SETTINGS_MODULE=django_settings

source env/bin/activate
coverage run -m unittest discover .
coverage report -m --skip-covered
