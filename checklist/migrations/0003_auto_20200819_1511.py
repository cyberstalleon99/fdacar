# Generated by Django 3.0.6 on 2020-08-19 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0020_auto_20200815_1411'),
        ('checklist', '0002_auto_20200516_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='inspection_type',
        ),
        migrations.AddField(
            model_name='job',
            name='job_type',
            field=models.CharField(choices=[('PLI', 'Post Licensing Inspection'), ('REN', 'Renewal of LTO'), ('FUP', 'Followup Inspection'), ('RTN', 'Routine Inspection')], max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='establishment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='masterlist.Establishment'),
        ),
        migrations.AlterField(
            model_name='job',
            name='inspection_status',
            field=models.CharField(choices=[('Complete', 'Complete'), ('Pending', 'Pending')], max_length=250),
        ),
    ]
