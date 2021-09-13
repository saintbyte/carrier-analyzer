import datetime
import functools
import json
import os

from bottle import HTTPError
from bottle import request

from constants import ACCESS_DENIED_STR
from constants import ACCESS_QUERYSTRING_PARAM
from constants import EXISTS_HC_VACANCIES_IDS_KEY
from redis_db import redis_connection


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj) -> str:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def get_exists_vacancies_ids():
    redis_result = redis_connection.get(EXISTS_HC_VACANCIES_IDS_KEY)
    if not redis_result:
        return []
    return [int(one_item) for one_item in redis_result.split(",")]


def set_exists_vacancies_ids(ids):
    redis_connection.set(EXISTS_HC_VACANCIES_IDS_KEY, ",".join(map(str, ids)))


def verify_access_by_magic_key(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if request.query.get(ACCESS_QUERYSTRING_PARAM) != os.environ.get(
            "ACCESS_MAGIC_KEY"
        ):
            raise HTTPError(status=403, body=ACCESS_DENIED_STR)
        return func(*args, **kwargs)

    return wrapper_decorator
