#!/bin/bash
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
python3 parser.py
