# Generated by Django 4.2 on 2025-03-09 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_usermodel_using_word_band_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='learning_time',
        ),
        migrations.RemoveField(
            model_name='userwordbandmodel',
            name='total_words',
        ),
    ]
