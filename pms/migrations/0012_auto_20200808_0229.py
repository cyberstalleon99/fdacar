# Generated by Django 3.0.6 on 2020-08-08 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0011_auto_20200808_0150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='analysis_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pms.AnalysisRequest', verbose_name='Analysis Request'),
        ),
    ]
