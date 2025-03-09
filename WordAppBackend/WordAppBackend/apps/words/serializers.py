from rest_framework import serializers

from users.models import UserWordBandModel, DailyRecordModel
from words.models import CategoryModel, WordBandModel, WordModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class WordBandSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True, label='词书创建时间')

    class Meta:
        model = WordBandModel
        exclude = ['update_time', 'creator']


class UserWordBandSerializer(serializers.ModelSerializer):
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
    word_band = WordBandSerializer(read_only=True)


class WordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = ('spelling', 'translations')


class WordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordModel
        fields = '__all__'


class DailyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRecordModel
        fields = '__all__'
