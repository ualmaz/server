# Generated by Django 2.2 on 2020-05-12 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200512_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='content',
        ),
    ]