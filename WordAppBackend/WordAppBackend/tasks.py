from celery import shared_task

from users.models import UserModel, UserWordBandModel


@shared_task
def clear():
    # 今日学习单词数目清零
    UserModel.objects.filter(today_words__gt=0).update(today_words=0)
    # 单词书清零
    UserWordBandModel.objects.filter(today_studied__gt=0).update(today_studied=0)
