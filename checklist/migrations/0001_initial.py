# Generated by Django 3.0.6 on 2020-05-12 02:15

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterlist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('inspection_status', models.CharField(default='pending', max_length=11)),
                ('inspection_type', models.CharField(choices=[('PLI', 'Post Licensing Inspection'), ('REN', 'Renewal of LTO'), ('INI', 'Initial Inspection'), ('RTN', 'Routine Inspection'), ('SPA', 'Special Assignment')], max_length=20, null=True)),
                ('establishment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='masterlist.Establishment')),
            ],
            managers=[
                ('renchecklist', django.db.models.manager.Manager()),
            ],
        ),
    ]
