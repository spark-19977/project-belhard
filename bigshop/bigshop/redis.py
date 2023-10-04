from django.conf import settings
from redis import Redis

redis = Redis.from_url(settings.REDIS_URL)