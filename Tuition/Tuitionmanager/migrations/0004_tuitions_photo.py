# Generated by Django 4.1.3 on 2024-04-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tuitionmanager', '0003_tuitions_slug_alter_tuitions_locality'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuitions',
            name='photo',
            field=models.ImageField(default=None, null=True, upload_to='tuitionphoto/'),
        ),
    ]