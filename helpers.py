import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj) -> str:
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
