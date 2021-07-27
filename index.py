import os

from bottle import hook
from bottle import route
from bottle import run
from bottle import template

from db import db

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


@route("/hello/<name>")
def index(name: str):
    return template("<b>Hello {{name}}</b>!", name=name)


run(host="0.0.0.0", port=int(os.environ.get("PORT")))
