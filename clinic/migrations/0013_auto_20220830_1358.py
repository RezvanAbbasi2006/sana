# Generated by Django 3.2.15 on 2022-08-30 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0012_delete_usergroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userreception',
            name='date',
        ),
        migrations.AddField(
            model_name='userreception',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Result', models.CharField(max_length=300, null=True)),
                ('reception', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic.userreception')),
            ],
        ),
    ]
