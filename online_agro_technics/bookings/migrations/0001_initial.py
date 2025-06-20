# Generated by Django 5.2.3 on 2025-06-20 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Басталу уақыты')),
                ('end_time', models.DateTimeField(verbose_name='Аяқталу уақыты')),
                ('is_available', models.BooleanField(default=True, verbose_name='Бос па')),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.servicetype', verbose_name='Қызмет түрі')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to=settings.AUTH_USER_MODEL, verbose_name='Жұмысшы')),
            ],
            options={
                'verbose_name': 'Жұмысшының бос уақыты',
                'verbose_name_plural': 'Жұмысшылардың бос уақыттары',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Күтуде'), ('confirmed', 'Растаулы'), ('cancelled', 'Жойылған')], default='pending', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Құрылған уақыты')),
                ('notes', models.TextField(blank=True, verbose_name='Ескертпелер')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('service_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.servicetype', verbose_name='Қызмет түрі')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_bookings', to=settings.AUTH_USER_MODEL, verbose_name='Жұмысшы')),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='bookings.workeravailability', verbose_name='Бос уақыт')),
            ],
            options={
                'verbose_name': 'Бронь',
                'verbose_name_plural': 'Броньдар',
            },
        ),
    ]
