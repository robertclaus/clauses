# Generated by Django 2.1.7 on 2019-08-09 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifttt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clause',
            name='user',
            field=models.TextField(blank=True, null=True),
        ),
    ]
