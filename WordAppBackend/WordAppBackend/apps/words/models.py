from django.db import models

from WordAppBackend.utils.base_model import BaseModel


# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='词书种类')
    order_number = models.IntegerField(verbose_name='排序字段', default=10)

    class Meta:
        db_table = 't_category'
        verbose_name = '词书类别表'
        verbose_name_plural = verbose_name
        ordering = ['order_number', 'id']

    def __str__(self):
        return self.name


class WordBandModel(BaseModel):
    name = models.CharField(max_length=50, verbose_name='词书名称')
    is_builtin = models.BooleanField(default=False, verbose_name='是否为内置词库')
    creator = models.ForeignKey('users.UserModel', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='词书的创建者')
    category = models.ForeignKey(CategoryModel, verbose_name='词书所属类别', on_delete=models.SET_NULL, null=True,
                                 blank=True)
    word_count = models.IntegerField(default=0, verbose_name='单词总数')

    class Meta:
        db_table = 't_word_bank'
        verbose_name = '词书表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class WordModel(models.Model):
    spelling = models.CharField(verbose_name='单词', max_length=100)
    translations = models.JSONField(verbose_name='翻译', null=True, blank=True)
    phrases = models.JSONField(verbose_name='短语', null=True, blank=True)
    relWords = models.JSONField(verbose_name='同根词', null=True, blank=True)
    sentences = models.JSONField(verbose_name='例句', null=True, blank=True)
    synonyms = models.JSONField(verbose_name='近义词', null=True, blank=True)
    ukphone = models.CharField(verbose_name='英音音标', max_length=100, null=True, blank=True)
    ukspeech = models.CharField(verbose_name='英音读音', max_length=300, null=True, blank=True)
    usphone = models.CharField(verbose_name='美音音标', max_length=100, null=True, blank=True)
    usspeech = models.CharField(verbose_name='美音读音', max_length=300, null=True, blank=True)

    class Meta:
        db_table = 't_word'
        verbose_name = '单词表'
        verbose_name_plural = verbose_name


class BandToWordModel(models.Model):
    band = models.ForeignKey(WordBandModel, on_delete=models.CASCADE, verbose_name='对应词书')
    word = models.ForeignKey(WordModel, on_delete=models.CASCADE, verbose_name='对应单词', related_name='bands')
    order_number = models.IntegerField(default=0, verbose_name='排序字段')

    class Meta:
        db_table = 't_band_word'
        verbose_name = '词书和单词对照表'
        verbose_name_plural = verbose_name
        ordering = ('order_number', 'id')
