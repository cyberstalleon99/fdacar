# Generated by Django 3.0.2 on 2020-02-25 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='establishment',
            name='radiologist',
        ),
        migrations.DeleteModel(
            name='Radiologist',
        ),
    ]
