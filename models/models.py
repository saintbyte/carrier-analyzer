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

    # Times
    created = DateTimeField(default=datetime.datetime.now)
    published = DateTimeField(null=True)  # entry.published_parsed
    updated = DateTimeField(null=True)  # entry.updated_parsed

    # SRC data
    src_title = CharField(default="")
    src_link = CharField(default="")
    src_author = CharField(default="")
    src_published = CharField(default="")
    src_summary = TextField(default="")
    src_updated = CharField(default="")
