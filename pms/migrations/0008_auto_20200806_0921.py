# Generated by Django 3.0.6 on 2020-08-06 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0007_auto_20200806_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='action',
            field=models.TextField(max_length=250, verbose_name='Action Take by RFO'),
        ),
        migrations.AlterField(
            model_name='product',
            name='analysis_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pms.AnalysisRequest', verbose_name='Analysis Request (For Lab Analysis only)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='remarks',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Remarks'),
        ),
    ]
