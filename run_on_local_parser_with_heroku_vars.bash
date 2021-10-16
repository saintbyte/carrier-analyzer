#!/bin/bash
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
python3 src/parser_hc.py
