# Generated by Django 3.0.2 on 2020-04-20 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0018_auto_20200420_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='specific_activity',
            field=models.ManyToManyField(to='masterlist.SpecificActivity'),
        ),
    ]