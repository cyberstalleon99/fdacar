# Generated by Django 3.0.3 on 2020-03-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0022_merge_20200311_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='date_inspected',
            field=models.DateTimeField(verbose_name='Date Inspected'),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='date_of_followup_inspection',
            field=models.DateTimeField(verbose_name='Date of Followup Inspection'),
        ),
        migrations.AlterField(
            model_name='lto',
            name='issuance',
            field=models.DateTimeField(blank=True, verbose_name='date issued'),
        ),
    ]
