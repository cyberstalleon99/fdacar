# Generated by Django 3.0.3 on 2020-04-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0002_cityormunicipality_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cityormunicipality',
            name='description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]