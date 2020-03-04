# Generated by Django 3.0.2 on 2020-02-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0004_auto_20200229_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='remarks',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='inspector',
            field=models.CharField(choices=[('GGM', 'Giovanni G. Monang'), ('RTB', 'Rochelle T. Bayanes'), ('NDN', 'Nadia D. Navarro'), ('SOP', 'Saturnina O. Pandosen')], max_length=3),
        ),
    ]
