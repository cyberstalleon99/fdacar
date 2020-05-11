# Generated by Django 3.0.3 on 2020-05-11 02:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import records.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('masterlist', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Capa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('approved_by', models.CharField(choices=[('GGM', 'Giovanni G. Monang'), ('RTB', 'Rochelle T. Bayanes'), ('NDN', 'Nadia D. Navarro'), ('SOP', 'Saturnina O. Pandosen')], max_length=10)),
                ('date_submitted', models.DateTimeField(verbose_name='date_submitted')),
                ('date_approved', models.DateTimeField(verbose_name='date_approved')),
                ('remarks', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_id', models.CharField(max_length=10, null=True, verbose_name='Folder Number')),
                ('establishment', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='masterlist.Establishment')),
            ],
        ),
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_number', models.CharField(max_length=14, null=True, verbose_name='DTN or Case #')),
                ('type_of_inspection', models.CharField(choices=[('PLI', 'Post Licensing Inspection'), ('REN', 'Renewal of LTO'), ('INI', 'Initial Inspection'), ('RTN', 'Routine Inspection')], max_length=20)),
                ('date_inspected', models.DateTimeField(verbose_name='Date Inspected')),
                ('frequency_of_inspection', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Frequency of Inspection')),
                ('risk_rating', models.CharField(blank=True, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=7, null=True)),
                ('date_of_followup_inspection', models.DateTimeField(blank=True, null=True, verbose_name='Date of Followup Inspection')),
                ('remarks', models.CharField(max_length=200, null=True)),
                ('inspection_report', models.FileField(null=True, upload_to=records.models.report_directory_path, verbose_name='Inspection Report')),
                ('capa', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='records.Capa')),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='records.Record', verbose_name='Record')),
            ],
            options={
                'ordering': ['-date_inspected'],
                'get_latest_by': 'date_inspected',
            },
        ),
        migrations.CreateModel(
            name='CapaPreparator',
            fields=[
                ('person_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='masterlist.Person')),
                ('capa', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='records.Capa')),
            ],
            options={
                'verbose_name': 'Preparedy by',
                'verbose_name_plural': 'Prepared by',
            },
            bases=('masterlist.person',),
        ),
        migrations.CreateModel(
            name='CapaDeficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('action', models.CharField(max_length=200)),
                ('evidence', models.FileField(blank=True, upload_to='')),
                ('type', models.CharField(choices=[('Critical', 'Critical'), ('Major', 'Major'), ('Others', 'Others')], max_length=10)),
                ('proposed_comletion_date', models.DateTimeField(verbose_name='Proposed Completion Date')),
                ('inspector_comment', models.CharField(blank=True, max_length=200)),
                ('accepted', models.BooleanField(default=False)),
                ('capa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='records.Capa')),
            ],
            options={
                'verbose_name': 'CAPA Deficiencies',
                'verbose_name_plural': 'CAPA Deficiencies',
            },
        ),
    ]
