# Generated by Django 3.0.6 on 2020-05-20 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0010_auto_20200517_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lto',
            name='expiry',
            field=models.DateField(help_text='Format: YYYY/MM/DD', verbose_name='expiry date'),
        ),
    ]