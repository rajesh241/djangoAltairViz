# Generated by Django 2.1.1 on 2019-06-23 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='batting',
            name='runs',
            field=models.IntegerField(default=0),
        ),
    ]
