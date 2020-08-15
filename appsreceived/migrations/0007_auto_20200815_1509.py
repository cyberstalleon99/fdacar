# Generated by Django 3.0.6 on 2020-08-15 15:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appsreceived', '0006_auto_20200815_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='date_forwarded_to_inspector',
            field=models.DateField(blank=True, null=True, verbose_name='Date Forwarded to Inspector'),
        ),
        migrations.AlterField(
            model_name='application',
            name='licensing_officer',
            field=models.ForeignKey(blank=True, default=7, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
