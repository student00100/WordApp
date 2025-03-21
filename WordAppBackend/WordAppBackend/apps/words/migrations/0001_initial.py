# Generated by Django 4.2 on 2025-03-08 14:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='词书种类')),
            ],
            options={
                'verbose_name': '词书类别表',
                'verbose_name_plural': '词书类别表',
                'db_table': 't_category',
            },
        ),
        migrations.CreateModel(
            name='WordModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=100, unique=True, verbose_name='单词')),
                ('translations', models.JSONField(blank=True, null=True, verbose_name='翻译')),
                ('phrases', models.JSONField(blank=True, null=True, verbose_name='短语')),
                ('relWords', models.JSONField(blank=True, null=True, verbose_name='同根词')),
                ('sentences', models.JSONField(blank=True, null=True, verbose_name='例句')),
                ('synonyms', models.JSONField(blank=True, null=True, verbose_name='近义词')),
                ('ukphone', models.CharField(blank=True, max_length=100, null=True, verbose_name='英音音标')),
                ('ukspeech', models.CharField(blank=True, max_length=300, null=True, verbose_name='英音读音')),
                ('usphone', models.CharField(blank=True, max_length=100, null=True, verbose_name='美音音标')),
                ('usspeech', models.CharField(blank=True, max_length=300, null=True, verbose_name='美音读音')),
            ],
            options={
                'verbose_name': '单词表',
                'verbose_name_plural': '单词表',
                'db_table': 't_word',
            },
        ),
        migrations.CreateModel(
            name='WordBankModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='词书种类')),
                ('is_builtin', models.BooleanField(default=False, verbose_name='是否为内置词库')),
                ('word_count', models.IntegerField(default=0, verbose_name='单词总数')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='words.categorymodel', verbose_name='词书所属类别')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='词书的创建者')),
            ],
            options={
                'verbose_name': '词书表',
                'verbose_name_plural': '词书表',
                'db_table': 't_word_bank',
            },
        ),
        migrations.CreateModel(
            name='BandToWordModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.IntegerField(default=0, verbose_name='排序字段')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.wordbankmodel', verbose_name='对应词书')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.wordmodel', verbose_name='对应单词')),
            ],
            options={
                'verbose_name': '词书和单词对照表',
                'verbose_name_plural': '词书和单词对照表',
                'db_table': 't_band_word',
                'ordering': ('order_number', 'id'),
            },
        ),
    ]
