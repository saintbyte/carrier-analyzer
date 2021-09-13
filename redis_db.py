import os

import redis

redis_connection = redis.from_url(os.environ.get("REDIS_URL"))
