# Generated by Django 3.2.7 on 2021-09-29 11:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20210929_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 9, 29, 11, 43, 54, 113708, tzinfo=utc), verbose_name='Время заказа'),
        ),
    ]
