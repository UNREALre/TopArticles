# Generated by Django 3.1.1 on 2020-09-22 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_usersource_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersource',
            name='label',
        ),
    ]
