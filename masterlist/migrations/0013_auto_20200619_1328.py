# Generated by Django 3.0.6 on 2020-06-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0012_auto_20200520_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='name',
            field=models.TextField(),
        ),
    ]