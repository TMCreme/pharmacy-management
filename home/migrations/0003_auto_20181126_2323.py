# Generated by Django 2.1.3 on 2018-11-26 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_medicine'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='generic_name',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='medicine',
            name='purchase_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
