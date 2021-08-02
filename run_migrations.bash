#!/bin/bash
set -x
export `heroku config -s | sed -e "s/='/=/" -e "s/'$//"`
pw_migrate migrate --database=$DATABASE_URL
