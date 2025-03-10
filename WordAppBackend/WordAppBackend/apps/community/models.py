from django.db import models

from WordAppBackend.utils.base_model import BaseModel


# Create your models here.
class CommunityPostModel(BaseModel):
    user = models.ForeignKey('users.UserModel', on_delete=models.CASCADE, related_name='posts')
    word = models.ForeignKey('words.WordModel', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(verbose_name='内容')
    like_count = models.IntegerField(default=0)

    # hot_score = models.FloatField(default=0.0)  # 热度分数

    class Meta:
        db_table = 't_post'
        verbose_name = '社区帖子表'
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)


class PostLikeModel(BaseModel):
    user = models.ForeignKey('users.UserModel', on_delete=models.CASCADE)
    post = models.ForeignKey(CommunityPostModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 't_user_post'
        unique_together = ('user', 'post')
