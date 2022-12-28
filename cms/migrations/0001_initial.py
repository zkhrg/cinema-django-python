# Generated by Django 3.2.7 on 2021-09-22 14:41

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
            name='Hall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('row_count', models.IntegerField(verbose_name='Количество рядов')),
                ('place_count', models.IntegerField(verbose_name='Количество мест в ряду')),
                ('photo', models.ImageField(upload_to='media/hall_photos/', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Зал',
                'verbose_name_plural': 'Залы',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('photo', models.ImageField(upload_to='media/movie_photos/', verbose_name='Фотография')),
                ('age_limit', models.IntegerField(verbose_name='Возрастное ограничение')),
            ],
            options={
                'verbose_name': 'Фильм',
                'verbose_name_plural': 'Фильмы',
            },
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time', models.TimeField(verbose_name='Время')),
                ('hall_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.hall', verbose_name='Зал')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.movie')),
            ],
            options={
                'verbose_name': 'Сеанс',
                'verbose_name_plural': 'Сеансы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Время заказа')),
                ('row_number', models.IntegerField(verbose_name='Номер ряда')),
                ('place_number', models.IntegerField(verbose_name='Номер места')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель')),
                ('seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.seance', verbose_name='Сеанс')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
