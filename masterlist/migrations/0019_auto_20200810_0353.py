# Generated by Django 3.0.6 on 2020-08-10 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0018_auto_20200810_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lto',
            name='type_of_application',
            field=models.CharField(blank=True, choices=[('Initial', 'Initial'), ('Renewal', 'Renewal'), ('Variation', 'Variation'), ('Re-Issuance', 'Re-Issuance')], max_length=20, null=True),
        ),
    ]
