# Generated by Django 2.1.3 on 2018-11-27 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20181127_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='category',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='sale',
            name='medicine',
            field=models.CharField(max_length=250),
        ),
    ]