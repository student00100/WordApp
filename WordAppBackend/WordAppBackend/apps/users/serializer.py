from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import UserModel
from users.utils import check_save_user_token
from words.serializers import UserWordBandSerializer, UserWordBandGetSerializer


class WXLoginUserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True, label='登录态token')

    class Meta:
        model = UserModel
        fields = ('id', 'nickname', 'token', 'avatar', 'studied_words',  'today_words')

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)


class WXAuthUserSerializer(serializers.ModelSerializer):
    """openid绑定用户的序列化器"""
    token = serializers.CharField(read_only=True, label='登录态的token')

    class Meta:
        model = UserModel
        fields = (
            'id', 'openid', 'nickname', 'avatar',
            'token')
        extra_kwargs = {
            'openid': {
                'required': True,
                'write_only': True,
            },
            'avatar': {
                'read_only': True,
            },
        }

    def validate(self, attrs):
        # 把加密的openid解密
        openid = attrs.get('openid')
        openid = check_save_user_token(openid)
        if openid is None:
            raise serializers.ValidationError('openid无效')
        attrs['openid'] = openid
        if UserModel.objects.filter(openid=openid).count() > 0:
            raise serializers.ValidationError('该微信已绑定用户')
        if UserModel.objects.filter(nickname=attrs['nickname']).count() > 0:
            raise serializers.ValidationError('用户昵称已存在')
        return attrs

    def create(self, validated_data):
        validated_data['username'] = validated_data['openid']
        # 创建用户
        user = UserModel.objects.create(**validated_data)
        # 生成JWT
        refresh = RefreshToken.for_user(user)
        user.token = str(refresh.access_token)
        return user


class UserInfoSerializer(serializers.ModelSerializer):
    using_word_band = UserWordBandGetSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'nickname', 'avatar', 'studied_words', 'today_words', 'using_word_band')
        extra_kwargs = {
            'nickname': {
                'read_only': True,
            },
            'studied_words': {
                'read_only': True,
            },
            # 'learning_time': {
            #     'read_only': True,
            # },
            'today_words': {
                'read_only': True,
            },
        }


class ModifyUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'avatar', 'using_word_band')


class Top20UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'nickname', 'avatar', 'studied_words', 'today_words')