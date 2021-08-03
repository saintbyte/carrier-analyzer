#!/bin/bash
set -x
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
export PORT=8800
echo "Run app on ${PORT}"
gunicorn index:app
