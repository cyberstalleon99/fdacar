# Generated by Django 3.0.6 on 2020-05-15 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masterlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishment',
            name='modified_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
