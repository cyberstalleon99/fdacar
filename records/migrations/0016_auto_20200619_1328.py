# Generated by Django 3.0.6 on 2020-06-19 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0015_auto_20200619_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capadeficiency',
            name='action',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='capadeficiency',
            name='inspector_comment',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
