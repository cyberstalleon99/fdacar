# Generated by Django 3.0.3 on 2020-05-08 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0011_auto_20200508_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='type_of_application',
        ),
    ]
