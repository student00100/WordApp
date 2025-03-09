from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # 原默认IP改为服务名
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_NAME = os.getenv('MYSQL_NAME', "innovation")
MYSQL_USER = os.getenv("MYSQL_USER", "innovation")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "NFnNwnfdimijZtsH")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_NAME,
        "HOST": MYSQL_HOST,
        "PORT": MYSQL_PORT,
        "PASSWORD": MYSQL_PASSWORD,
        "USER": MYSQL_USER,
        "OPTIONS": {
            "init_command": "SET foreign_key_checks = 0;",
            "charset": "utf8mb4",
        },
        'CONN_MAX_AGE': 300,
        'POOL_OPTIONS': {
            'MAX_CONNS': 30,  # 最大连接数
            'MAX_LIFETIME': 7200,  # 连接的最大生命周期
            'RECYCLE_INTERVAL': 3600  # 新增回收间隔
        },
    }
}

REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # 原默认IP改为服务名
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "4"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "GGsYPKLbLGRDDTpR")
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # access_token
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "access_token": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
# Broker配置，使用Redis作为消息中间件
BROKER_URL = 'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/3'
# BACKEND配置，使用Redis作为结果仓库
RESULT_BACKEND = 'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/4'
WX_APPID = 'wxb531bffe27fd4e8b'
WX_SECRET = 'e124b8542df78972af57071de5097704'
