# Generated by Django 3.0.2 on 2020-04-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0009_auto_20200409_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='checklist_status',
            field=models.CharField(default='hidden', max_length=9, null=True),
        ),
        migrations.AlterField(
            model_name='establishment',
            name='inspection_status',
            field=models.CharField(default='pending', max_length=11, null=True),
        ),
    ]
