import datetime
import functools
import json
import os

from bottle import HTTPError
from bottle import request
from constants import ACCESS_DENIED_STR
from constants import ACCESS_QUERYSTRING_PARAM


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj) -> str:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def verify_access_by_magic_key(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if request.query.get(ACCESS_QUERYSTRING_PARAM) != os.environ.get(
            "ACCESS_MAGIC_KEY"
        ):
            raise HTTPError(status=403, body=ACCESS_DENIED_STR)
        return func(*args, **kwargs)

    return wrapper_decorator
