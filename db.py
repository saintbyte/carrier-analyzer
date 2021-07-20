import os

from playhouse.db_url import connect

db_connection = connect(os.environ.get("DATABASE_URL"))
