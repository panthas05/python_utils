#!/bin/bash
cd $( dirname $0 )
cd ../

export DJANGO_SETTINGS_MODULE=django_settings

source env/bin/activate
python3 -m unittest discover .