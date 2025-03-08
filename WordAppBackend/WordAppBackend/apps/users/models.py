from django.contrib.auth.models import AbstractUser
from django.db import models

from WordAppBackend.utils.base_model import BaseModel


# Create your models here.
class UserModel(AbstractUser):
    nickname = models.CharField(verbose_name='昵称', max_length=50, unique=True)
    avatar = models.FileField(upload_to='avatars', default='avatars/default_avatar.jpg')
    openid = models.CharField(verbose_name='微信openid', max_length=100, unique=True)
    # learning_goal = models.TextField(verbose_name='学习目标')
    studied_words = models.IntegerField(default=0)  # 已学单词数
    learning_time = models.DurationField(default=0)  # 学习时长
    today_words = models.IntegerField(default=0, verbose_name='今日学习单词数')

    class Meta:
        db_table = 't_users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname


class UserWordBandModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='所属用户')
    word_band = models.ForeignKey('words.WordBankModel', on_delete=models.CASCADE, verbose_name='对应的词书')
    study_words = models.IntegerField(default=0, verbose_name='已学单词')
    total_words = models.IntegerField(default=0, verbose_name='总单词数')
    daily_goal = models.IntegerField(default=20, verbose_name='每日学习目标')

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
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户')
    word = models.ForeignKey('words.WordModel', on_delete=models.CASCADE, verbose_name='单词')
    error_count = models.IntegerField(default=1, verbose_name='错误次数')
    last_error_time = models.DateTimeField(auto_now=True, verbose_name='最后错误时间')

    class Meta:
        db_table = 't_error_word'
        unique_together = ('user', 'word')
        verbose_name = '错题本'
        verbose_name_plural = verbose_name


class DailyRecordModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户')
    date = models.DateField(auto_now_add=True, verbose_name='记录日期')
    new_words = models.IntegerField(default=0, verbose_name='新学单词')
    review_words = models.IntegerField(default=0, verbose_name='复习单词')

    class Meta:
        db_table = 't_daily_record'
        verbose_name = '每日学习记录'
        verbose_name_plural = verbose_name
