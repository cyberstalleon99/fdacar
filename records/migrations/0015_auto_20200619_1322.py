# Generated by Django 3.0.6 on 2020-06-19 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0014_auto_20200619_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capa',
            name='recommendation',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='capa',
            name='remarks',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
