# Generated by Django 3.0.6 on 2020-05-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0004_auto_20200515_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishment',
            name='status',
            field=models.CharField(choices=[('Inactive', 'Inactive'), ('Active', 'Active')], default='Active', max_length=8, null=True),
        ),
    ]
