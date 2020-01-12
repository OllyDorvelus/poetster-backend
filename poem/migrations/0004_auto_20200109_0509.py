# Generated by Django 2.2.8 on 2020-01-09 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0003_poem_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='genre',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]