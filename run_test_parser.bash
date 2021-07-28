#!/bin/bash
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
export RSS_URL="https://career.habr.com/vacancies/rss?type=all"
export DEBUG=1
python3 parser.py
