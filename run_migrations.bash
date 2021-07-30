#!/bin/bash
set -x
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
export RSS_URL="https://career.habr.com/vacancies/rss?type=all"
export DEBUG=1
pw_migrate migrate --database=$DATABASE_URL
