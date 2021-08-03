import json
import os

import bottle
from bottle import hook
from bottle import response
from bottle import route
from bottle import run

from db import db
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


"""
Routes
"""


@route("/count/")
def count_items():
    cnt = Vacancy.select().count()
    response.content_type = "application/json"
    return json.dumps({"count": cnt})


@route("/")
def index():
    return "<h1>Its working!</h1>"


if __name__ == "__main__":
    run(host="0.0.0.0", port=int(os.environ.get("PORT")))
app = bottle.default_app()
