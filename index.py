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

from db import db
from models import Vacancy

ACCESS_DENIED_STR: str = "Access Denied"
CORS_ALL_WILDCARD: str = "*"
CORS_ALLOWED_HTTP_METHODS: str = "GET, POST, PUT, OPTIONS"
CORS_ALLOWED_HTTP_HEADERS: str = (
    "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token"
)
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
    if request.query.get("access_token") != os.environ("ACCESS_MAGIC_KEY", None):
        raise HTTPError(status=403, body=ACCESS_DENIED_STR)
    return json.dumps(model_to_dict(Vacancy.select()))


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
    response.content_type = "application/json"
    return json.dumps({str(row.date): row.count for row in query})


@route("/count/")
def count_items():
    cnt = Vacancy.select().count()
    response.content_type = "application/json"
    return json.dumps({"count": cnt})


@route("/")
def index():
    return "<h1>Its working!</h1>"


app = bottle.default_app()

if __name__ == "__main__":
    run(host="0.0.0.0", port=int(os.environ.get("PORT")))
