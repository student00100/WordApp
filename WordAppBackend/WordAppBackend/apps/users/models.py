from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from WordAppBackend.utils.base_model import BaseModel


# Create your models here.
class UserModel(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=50, unique=True)
    avatar = models.FileField(upload_to='avatars', default='avatars/default_avatar.jpg')
    openid = models.CharField(verbose_name='微信openid', max_length=100, unique=True)
    # learning_goal = models.TextField(verbose_name='学习目标')
    studied_words = models.IntegerField(default=0)  # 已学单词数
    # learning_time = models.IntegerField(default=0)  # 学习时长
    today_words = models.IntegerField(default=0, verbose_name='今日学习单词数')
    using_word_band = models.ForeignKey('UserWordBandModel', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 't_users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class UserWordBandModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='所属用户', related_name='word_bands')
    word_band = models.ForeignKey('words.WordBandModel', on_delete=models.CASCADE, verbose_name='对应的词书')
    study_words = models.IntegerField(default=0, verbose_name='已学单词')
    # total_words = models.IntegerField(default=0, verbose_name='总单词数')
    daily_goal = models.IntegerField(default=20, verbose_name='每日学习目标')
    today_studied = models.IntegerField(default=0, verbose_name='今日学习数')

    class Meta:
        db_table = 't_user_word_band'
        verbose_name = '用户词书表'
        verbose_name_plural = verbose_name


class UserWordRecordModel(models.Model):
    MEMORY_STAGES = [
        (0, '未开始'),
        (1, '阶段1'),
        (2, '阶段2'),
        (3, '阶段3'),
        (4, '阶段4'),
        (5, '已掌握')
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户')
    word = models.ForeignKey('words.WordModel', on_delete=models.CASCADE, verbose_name='单词')
    memory_stage = models.IntegerField(choices=MEMORY_STAGES, default=0)
    next_review = models.DateTimeField(verbose_name='下次复习时间')
    correct_count = models.IntegerField(default=0, verbose_name='正确次数')
    wrong_count = models.IntegerField(default=0, verbose_name='错误次数')
    last_reviewed = models.DateTimeField(auto_now=True, verbose_name='最后复习时间')

    class Meta:
        db_table = 't_user_word_record'
        unique_together = ('user', 'word')
        verbose_name = '用户单词记录'
        verbose_name_plural = verbose_name


class ErrorWordModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户', related_name='error_words')
    word = models.ForeignKey('words.WordModel', on_delete=models.CASCADE, verbose_name='单词')
    error_count = models.IntegerField(default=1, verbose_name='错误次数')
    track_correct_count = models.IntegerField(default=0)  # 追踪正确次数
    correct_threshold = models.IntegerField(default=3)  # 正确达标阈值
    next_review = models.DateTimeField(default=timezone.now)  # 下次建议复习时间

    class Meta:
        db_table = 't_error_word'
        unique_together = ('user', 'word')
        verbose_name = '错题本'
        verbose_name_plural = verbose_name


class DailyRecordModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户', related_name='daily_records')
    date = models.DateField(auto_now_add=True, verbose_name='记录日期')
    new_words = models.IntegerField(default=0, verbose_name='新学单词')
    review_words = models.IntegerField(default=0, verbose_name='复习单词')

    class Meta:
        db_table = 't_daily_record'
        verbose_name = '每日学习记录'
        verbose_name_plural = verbose_name
