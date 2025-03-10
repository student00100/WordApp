from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from WordAppBackend.utils.paginations import GlobalPagination
from community.models import CommunityPostModel, PostLikeModel
from community.serializers import CommunitySerializer


# Create your views here.

class CommunityViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = CommunitySerializer
    queryset = CommunityPostModel.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = GlobalPagination

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            return Response({'detail': "你不能删除别人的帖子"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            like = PostLikeModel.objects.get(user=request.user, post=obj)
            like.delete()
        except PostLikeModel.DoesNotExist:
            PostLikeModel.objects.create(user=request.user, post=obj)
        return Response({"message": "ok"})