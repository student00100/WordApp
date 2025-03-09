from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'root',  # 数据库用户密码
        'NAME': 'wordApp'  # 数据库名字
    }
}
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "verify_code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

# 微信小程序
WX_APPID = 'wxb531bffe27fd4e8b'
WX_SECRET = 'e124b8542df78972af57071de5097704'
# Broker配置，使用Redis作为消息中间件
BROKER_URL = 'redis://127.0.0.1:6379/1'
# BACKEND配置，使用Redis作为结果仓库
RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
