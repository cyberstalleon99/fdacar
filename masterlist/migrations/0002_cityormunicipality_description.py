# Generated by Django 3.0.3 on 2020-04-07 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cityormunicipality',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
    ]