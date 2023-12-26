# Generated by Django 4.1.3 on 2023-07-26 12:35

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tuitions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_date', models.DateField(default=datetime.datetime.now)),
                ('status', models.BooleanField(default=True)),
                ('student_name', models.CharField(blank=True, max_length=20, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True)),
                ('course', models.CharField(blank=True, max_length=25, null=True)),
                ('subject', models.CharField(blank=True, max_length=25, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('teaching_mode', models.CharField(max_length=10)),
                ('fee', models.CharField(blank=True, max_length=10, null=True)),
                ('locality', models.CharField(blank=True, max_length=60, null=True)),
                ('unlocks', models.IntegerField(blank=True, default=0, null=True)),
                ('verify', models.BooleanField(default=False)),
                ('pincode', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='Home.pincodes')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tuition_unlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unlock_date', models.DateField(default=datetime.datetime.now)),
                ('Tuition_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tuitionmanager.tuitions')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
