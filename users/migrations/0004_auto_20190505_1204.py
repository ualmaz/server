# Generated by Django 2.2 on 2019-05-05 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_post_social'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='social',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Social Media'),
        ),
    ]
