# Generated by Django 2.1.3 on 2018-11-28 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20181128_0218'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='invoice_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.SalesInvoice'),
            preserve_default=False,
        ),
    ]
