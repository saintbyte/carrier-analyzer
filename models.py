import datetime

from peewee import AutoField
from peewee import BigIntegerField
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model
from peewee import TextField
from playhouse.postgres_ext import ArrayField

from db import db


class BaseModel(Model):
    class Meta:
        database = db


class Vacancy(BaseModel):
    id = AutoField(primary_key=True)
    vacancy_id = BigIntegerField(unique=True)
    job_title = CharField()
    developer_level = CharField(blank=True)
    town = CharField(blank=True)
    salary_start = IntegerField(default=0, blank=True)
    salary_end = IntegerField(default=0, blank=True)
    salary_currency = CharField(blank=True)
    is_fulltime = BooleanField(default=False)
    is_remote = BooleanField(default=False)
    company_name = CharField(blank=True)
    skills = ArrayField(CharField, default=[])

    # Times
    created = DateTimeField(default=datetime.datetime.now)
    published = DateTimeField(null=True)  # entry.published_parsed
    updated = DateTimeField(null=True)  # entry.updated_parsed

    # SRC data
    src_title = CharField(blank=True)
    src_link = CharField(blank=True)
    src_author = CharField(blank=True)
    src_published = CharField(blank=True)
    src_summary = TextField(blank=True)
    src_updated = CharField(blank=True)
