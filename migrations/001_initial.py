import os
import sys

sys.path.append(os.path.dirname("./"))
sys.path.append(os.path.dirname("../"))

import peewee as pw
from models import Vacancy

SQL = pw.SQL


def migrate(migrator, database, fake=False, **kwargs):
    migrator.create_model(Vacancy)


def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model(Vacancy)
