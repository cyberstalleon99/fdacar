# Generated by Django 3.0.3 on 2020-05-08 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0002_auto_20200508_1154'),
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='establishment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterlist.Establishment'),
        ),
    ]
