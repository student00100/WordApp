import requests
from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, BadSignature


def get_open_id(appid, secret, js_code):
    # 构建请求url
    url = ('https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + js_code +
           '&grant_type=authorization_code')
    # 发送请求
    try:
        response = requests.get(url)
        data = response.json()
    except:
        return {'errmsg': '请求WX失败'}

    return data


def generate_save_user_token(openid):
    """对openid进行加密"""
    # 1. 创建序列化器对象
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    # 2.调用dumps进行加密
    data = {'openid': openid}
    token = serializer.dumps(data)
    # 3. 返回加密后的openid
    return token


def check_save_user_token(openid):
    """对openid进行解密"""
    # 1. 创建序列化器对象
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
    # 2.调用loads进行加密
    # data = {'openid': openid}
    try:
        token = serializer.loads(openid)
        # data = serializer.loads(token, max_age=expiration)
    except BadSignature:
        return None
    # 3. 返回解密后的openid
    return token.get('openid')
