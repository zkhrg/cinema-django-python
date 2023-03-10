# Generated by Django 3.2.7 on 2021-09-27 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='place_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='row_number',
        ),
        migrations.RemoveField(
            model_name='order',
            name='seance',
        ),
        migrations.AddField(
            model_name='seance',
            name='base_price',
            field=models.IntegerField(null=True, verbose_name='Цена'),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row_number', models.IntegerField(verbose_name='Номер ряда')),
                ('place_number', models.IntegerField(verbose_name='Номер места')),
                ('status', models.BooleanField(verbose_name='Статус')),
                ('seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.seance', verbose_name='Сеанс')),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.ticket', verbose_name='Билет'),
        ),
    ]
