# Generated by Django 3.0.6 on 2020-07-30 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pli', '0002_auto_20200730_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pli',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pli.PliStatus'),
        ),
    ]
