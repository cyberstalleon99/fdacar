# Generated by Django 3.0.3 on 2020-04-08 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0004_auto_20200407_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='tracking_number',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='remarks',
            field=models.CharField(max_length=200, null=True),
        ),
    ]