from rest_framework import serializers

from community.models import CommunityPostModel, PostLikeModel


class CommunitySerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommunityPostModel
        fields = '__all__'
        extra_kwargs = {
            'like_count': {
                'read_only': True,
            },
            'user': {
                'read_only': True,
            }
        }

    def get_is_like(self, obj):
        return PostLikeModel.objects.filter(user=self.context['request'].user, post=obj).exists()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

