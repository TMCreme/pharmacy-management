# Generated by Django 2.1.3 on 2018-11-28 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_salesinvoice_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesinvoice',
            name='user',
        ),
    ]