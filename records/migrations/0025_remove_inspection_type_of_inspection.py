# Generated by Django 3.0.6 on 2020-08-23 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0024_auto_20200822_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inspection',
            name='type_of_inspection',
        ),
    ]
