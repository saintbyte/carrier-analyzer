import os

from bottle import route
from bottle import run
from bottle import template


@route("/hello/<name>")
def index(name: str):
    return template("<b>Hello {{name}}</b>!", name=name)


run(host="0.0.0.0", port=int(os.environ.get("PORT")))
