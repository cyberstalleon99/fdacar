# Generated by Django 3.0.6 on 2020-10-19 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appsreceived', '0009_auto_20200904_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='remarks',
            field=models.TextField(blank=True, null=True, verbose_name='Remarks (for manual apps only)'),
        ),
    ]
