# Generated by Django 3.0.6 on 2020-07-31 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pli', '0004_auto_20200730_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pli',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pli.PliStatus'),
        ),
    ]
