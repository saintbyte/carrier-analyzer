import datetime
import json

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
