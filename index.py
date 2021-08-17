import json
import os

import bottle
from bottle import hook
from bottle import HTTPError
from bottle import request
from bottle import response
from bottle import route
from bottle import run
from bottle import template
from peewee import fn
from playhouse.shortcuts import model_to_dict

from constants import ACCESS_DENIED_STR
from constants import ACCESS_QUERYSTRING_PARAM
from constants import CORS_ALL_WILDCARD
from constants import CORS_ALLOWED_HTTP_HEADERS
from constants import CORS_ALLOWED_HTTP_METHODS
from constants import JSON_CONTENT_TYPE
from db import db
from helpers import DateTimeEncoder
from models import Vacancy

"""
Enable Sentry if needed
"""
if all(
    [
        os.environ.get("SENTRY_KEY"),
        os.environ.get("SENTRY_PROJECT"),
    ]
):
    import sentry_sdk
    from sentry_sdk.integrations.bottle import BottleIntegration

    sentry_sdk.init(
        dsn="https://{SENTRY_KEY}@sentry.io/{SENTRY_PROJECT}".format(**os.environ),
        integrations=[BottleIntegration()],
    )


"""
Hook for databases
"""


@hook("before_request")
def _connect_db():
    db.connect(reuse_if_open=True)


@hook("after_request")
def _close_db():
    if not db.is_closed():
        db.close()


@hook("after_request")
def _enable_cors():
    response.headers["Access-Control-Allow-Origin"] = CORS_ALL_WILDCARD
    response.headers["Access-Control-Allow-Methods"] = CORS_ALLOWED_HTTP_METHODS
    response.headers["Access-Control-Allow-Headers"] = CORS_ALLOWED_HTTP_HEADERS


"""
Routes
"""


@route("/export-vacancy/")
def export_vacancy():
    if request.query.get(ACCESS_QUERYSTRING_PARAM) != os.environ.get(
        "ACCESS_MAGIC_KEY"
    ):
        raise HTTPError(status=403, body=ACCESS_DENIED_STR)
    response.content_type = JSON_CONTENT_TYPE
    return json.dumps([model_to_dict(v) for v in Vacancy.select()], cls=DateTimeEncoder)


@route("/count-by-date-chart/")
def count_by_days_chart():
    return template("templates/count_by_date.html")


@route("/count-by-date/")
def count_by_days():
    query = (
        Vacancy.select(
            fn.date_trunc("day", Vacancy.created).alias("date"),
            fn.COUNT("date").alias("count"),
        )
        .group_by(fn.date_trunc("day", Vacancy.created))
        .order_by(fn.date_trunc("day", Vacancy.created))
    )
    response.content_type = JSON_CONTENT_TYPE
    return json.dumps({str(row.date): row.count for row in query})


@route("/count/")
def count_items():
    cnt = Vacancy.select().count()
    response.content_type = JSON_CONTENT_TYPE
    return json.dumps({"count": cnt})


@route("/")
def index():
    return "<h1>Its working!</h1>"


app = bottle.default_app()

if __name__ == "__main__":
    run(host="0.0.0.0", port=int(os.environ.get("PORT")))
