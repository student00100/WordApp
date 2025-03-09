import logging

from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import UserModel
from users.serializer import WXAuthUserSerializer, WXLoginUserSerializer, UserInfoSerializer, ModifyUserInfoSerializer, \
    Top20UserSerializer
from users.utils import get_open_id, generate_save_user_token

logger = logging.getLogger('word')


# Create your views here.
class WXAuthUserView(CreateAPIView):
    """
    get:
    根据微信登录的code获取openid

    post:
    微信绑定用户

    传入加密后的openid和微信获取的手机号code，绑定到已经录入的用户，如果没有用户与之对应，则会新建用户
    """
    serializer_class = WXAuthUserSerializer

    def get(self, request, *args, **kwargs):
        # 1. 获取前端传入参数
        code = request.query_params.get('code', None)
        if not code:
            return Response(data={"detail": "缺少code"}, status=status.HTTP_400_BAD_REQUEST)
        data = get_open_id(settings.WX_APPID, settings.WX_SECRET, code)
        openid = data.get('openid')
        if not openid:
            logger.error(data.get("errmsg", 'WX登录失败'))
            return Response(data={"detail": data.get("errmsg", 'WX登录失败')},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            user = UserModel.objects.get(openid=openid)
        except UserModel.DoesNotExist:
            # 没有绑定用户
            # 需要对openid进行加密
            openid = generate_save_user_token(openid)
            return Response({'openid': openid})
        else:
            # 已经绑定用户
            # refresh = RefreshToken.for_user(user)
            # token = {'refresh': str(refresh),
            #          'access': str(refresh.access_token)
            #          }
            result_data = WXLoginUserSerializer(instance=user).data
            return Response(result_data)


class UserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ModifyUserInfoSerializer

    def get(self, request, *args, **kwargs):
        return Response(UserInfoSerializer(instance=request.user).data)

    def post(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetTop20UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        is_today = request.query_params.get('is_today', None)
        if is_today:
            users = UserModel.objects.order_by('-today_words')[:20]
        else:
            users = UserModel.objects.order_by('-studied_words')[:20]

        return Response(Top20UserSerializer(users, many=True).data)
