# Generated by Django 4.2 on 2025-03-09 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0002_alter_categorymodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordmodel',
            name='frequency',
            field=models.FloatField(default=0),
        ),
    ]
