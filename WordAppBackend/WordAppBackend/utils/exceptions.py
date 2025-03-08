from rest_framework.views import exception_handler as drf_exception_handler
import logging
from django.db import DatabaseError
from redis.exceptions import RedisError
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('django')


def exception_handler(exc, context):
    """
    自定异常捕获
    :param exc:异常
    :param context:抛出异常的上下文(包括request和view对象)
    :return: Response响应对象
    """
    response = drf_exception_handler(exc, context)
    if response is None:
        view = context.get('view')
        if isinstance(exc, DatabaseError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({"message": "Mysql服务器数据库异常"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        elif isinstance(exc, RedisError):
            # 数据库异常
            logger.error('[%s] %s' % (view, exc))
            response = Response({"message": "Redis服务器数据库异常"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
    return response
