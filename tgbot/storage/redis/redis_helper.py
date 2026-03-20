from redis.asyncio import Redis

from config import settings


class RedisHelper:
    def __init__(self):
        self.redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
            db=settings.redis.path.split("/")[1],
        )

    def get_redis(self):
        return self.redis


redis_helper = RedisHelper()
