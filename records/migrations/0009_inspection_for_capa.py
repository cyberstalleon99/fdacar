# Generated by Django 3.0.6 on 2020-05-21 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_auto_20200520_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='for_capa',
            field=models.BooleanField(default=False),
        ),
    ]
