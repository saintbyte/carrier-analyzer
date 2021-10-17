from __future__ import annotations

import datetime

from constants import EXISTS_HC_VACANCIES_IDS_KEY
from peewee import AutoField
from peewee import BigIntegerField
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import TextField
from playhouse.postgres_ext import ArrayField
from redis_db import redis_connection

from .base import BaseModel


class Vacancy(BaseModel):
    id = AutoField(primary_key=True)
    vacancy_id = BigIntegerField(unique=True)
    job_title = CharField(null=True)
    developer_level = CharField(default="", null=True)
    town = CharField(default="", null=True)
    salary_start = IntegerField(default=0, null=True)
    salary_end = IntegerField(default=0, null=True)
    salary_currency = CharField(default="", null=True)
    is_fulltime = BooleanField(default=False, null=True)
    is_remote = BooleanField(default=False, null=True)
    company_name = CharField(default="", null=True)
    skills = ArrayField(CharField, default=[], null=True)
    created = DateTimeField(default=datetime.datetime.now)
    published = DateTimeField(null=True)
    updated = DateTimeField(null=True)
    src_title = CharField(default="")
    src_link = CharField(default="")
    src_author = CharField(default="")
    src_published = CharField(default="")
    src_summary = TextField(default="")
    src_updated = CharField(default="")

    @staticmethod
    def get_exists_vacancies_ids() -> list[int]:
        redis_result = redis_connection.get(EXISTS_HC_VACANCIES_IDS_KEY)
        if not redis_result:
            return []
        redis_result = redis_result.decode("utf-8")
        if "," not in redis_result:
            return [
                int(redis_result),
            ]
        return [int(one_item) for one_item in redis_result.split(",")]

    @staticmethod
    def set_exists_vacancies_ids(ids: list):
        redis_connection.set(EXISTS_HC_VACANCIES_IDS_KEY, ",".join(map(str, ids)))
