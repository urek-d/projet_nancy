# Generated by Django 4.2 on 2023-04-11 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lieu',
            name='nom',
            field=models.CharField(default='unkozn', max_length=255),
        ),
    ]
