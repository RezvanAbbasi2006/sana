# Generated by Django 3.2.15 on 2022-09-01 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0017_userprofile_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='token',
        ),
    ]
