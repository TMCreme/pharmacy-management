# Generated by Django 2.1.3 on 2018-12-03 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20181129_0346'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expensecategory',
            options={'verbose_name_plural': 'expensecategories'},
        ),
        migrations.AlterField(
            model_name='medicine',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]
