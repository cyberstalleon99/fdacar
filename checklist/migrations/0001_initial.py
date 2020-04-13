# Generated by Django 3.0.2 on 2020-04-11 14:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterlist', '0010_auto_20200411_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date modified')),
                ('inspecion_status', models.CharField(max_length=11)),
                ('establishment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterlist.Establishment')),
            ],
        ),
    ]
