from django.db import models


class BaseModel(models.Model):
    """
    所有模型的父类，公共属性
    """
    # auto_now_add:插入时添加
    # auto_now:只要更改就添加
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        abstract = True  # 抽象类， 不需要映射
