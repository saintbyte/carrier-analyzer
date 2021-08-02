import os

from playhouse.db_url import connect

db = connect(os.environ.get("DATABASE_URL"), autocommit=True, autorollback=True)
