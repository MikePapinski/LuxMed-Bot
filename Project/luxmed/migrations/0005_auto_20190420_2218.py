# Generated by Django 2.2 on 2019-04-20 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luxmed', '0004_auto_20190419_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mytask',
            name='TimeFrom',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='mytask',
            name='TimeTo',
            field=models.TimeField(),
        ),
    ]
