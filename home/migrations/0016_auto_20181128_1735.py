# Generated by Django 2.1.3 on 2018-11-28 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_salesinvoice_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='medicinecategory',
            options={'ordering': ('category',), 'verbose_name': 'medicinecategory', 'verbose_name_plural': 'medicinecategories'},
        ),
        migrations.AlterField(
            model_name='expense',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
    ]
