# Generated by Django 3.2.7 on 2021-09-28 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20210927_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_slug',
            field=models.SlugField(blank='movie', max_length=60, verbose_name='Ссылка'),
        ),
        migrations.AddField(
            model_name='seance',
            name='seance_slug',
            field=models.SlugField(blank='seance', max_length=60, verbose_name='Ссылка'),
        ),
    ]
