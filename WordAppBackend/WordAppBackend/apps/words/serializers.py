from rest_framework import serializers

from users.models import UserWordBandModel, DailyRecordModel, ErrorWordModel
from words.models import CategoryModel, WordBandModel, WordModel


class CategorySerializer(serializers.ModelSerializer):
    """词书类别序列化"""
    class Meta:
        model = CategoryModel
        fields = '__all__'


class WordBandSerializer(serializers.ModelSerializer):
    """词书的序列化"""
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='词书创建时间')

    class Meta:
        model = WordBandModel
        exclude = ['update_time', 'creator']


class UserWordBandSerializer(serializers.ModelSerializer):
    """用户词书创建/修改序列化"""
    # word_band = WordBandSerializer(read_only=True)

    class Meta:
        model = UserWordBandModel
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            'study_words': {
                'read_only': True
            },
        }

    def create(self, validated_data):
        if UserWordBandModel.objects.filter(user=self.context['request'].user,
                                            word_band=validated_data['word_band']).exists():
            raise serializers.ValidationError('用户单词书已存在')
        validated_data['user'] = self.context['request'].user
        instance = super().create(validated_data)
        self.context['request'].user.using_word_band = instance
        self.context['request'].user.save()
        return instance


class UserWordBandGetSerializer(UserWordBandSerializer):
    """用户词书获取序列化"""
    word_band = WordBandSerializer(read_only=True)


class WordListSerializer(serializers.ModelSerializer):
    """获取单词列表序列化"""
    class Meta:
        model = WordModel
        fields = ('spelling', 'translations')


class WordDetailSerializer(serializers.ModelSerializer):
    """获取单个单词序列化"""
    class Meta:
        model = WordModel
        fields = '__all__'


class DailyRecordSerializer(serializers.ModelSerializer):
    """每日单词记忆记录序列化器类"""
    class Meta:
        model = DailyRecordModel
        fields = '__all__'


class ErrorWordSerializer(serializers.ModelSerializer):
    """错误单词序列化类"""
    word = WordListSerializer(read_only=True)

    class Meta:
        model = ErrorWordModel
        fields = '__all__'
