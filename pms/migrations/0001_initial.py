# Generated by Django 3.0.6 on 2020-08-04 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('masterlist', '0014_auto_20200729_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='DosageForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ReferralType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_collected', models.DateField(verbose_name='Date Collected')),
                ('tracking_number', models.CharField(max_length=12, verbose_name='DTN/Case No.')),
                ('date_request_received', models.DateField(blank=True, null=True, verbose_name='Date of Request Letter Received')),
                ('date_of_referral', models.DateField(verbose_name='Date of Referral')),
                ('generic_name', models.CharField(max_length=250, verbose_name='Generic Name')),
                ('brand_name', models.CharField(max_length=250, verbose_name='Brand Name')),
                ('cpr_number', models.CharField(max_length=250, verbose_name='CPR No.')),
                ('batch_lot_number', models.CharField(max_length=250, verbose_name='Batch/Lot No.')),
                ('date_manufactured', models.DateField(verbose_name='Manufacuring Date')),
                ('date_exiry', models.DateField(verbose_name='Expiration Date')),
                ('tmr_name', models.CharField(max_length=250, verbose_name="Trader/Mfg/Repacker's Name")),
                ('tmr_address', models.TextField(verbose_name="Trader/Mfg/Repacker's Address")),
                ('distributor_name', models.CharField(max_length=250, verbose_name="Distributor's Name")),
                ('distributor_address', models.TextField(verbose_name="Distributor's Address")),
                ('remarks', models.DateField(verbose_name='Remarks')),
                ('quantity', models.PositiveIntegerField(verbose_name='Number of Samples')),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('or_number', models.CharField(max_length=250, verbose_name='OR Number')),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_forwarded', models.DateField()),
                ('date_result_received', models.DateField()),
                ('result', models.TextField()),
                ('csl_reference_number', models.CharField(max_length=250, verbose_name='CSL Control Ref. No.')),
                ('center_remarks', models.TextField(verbose_name='Remarks of Centers')),
                ('action', models.CharField(max_length=250, verbose_name='Action Take by RFO')),
                ('warning_letter', models.CharField(blank=True, max_length=250, null=True)),
                ('analysis_request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.AnalysisRequest', verbose_name='Analysis Request (For Lab Analysis only)')),
                ('classification', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.Classification', verbose_name='PMS Classification')),
                ('collection_mode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.CollectionMode', verbose_name='Mode of Collection')),
                ('dosage_form', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.DosageForm', verbose_name='Dosage Form')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='masterlist.Establishment', verbose_name='Establishment')),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Inspector')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.ProductCategory', verbose_name='Product Category')),
                ('type_of_referral', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.ReferralType', verbose_name='Type of Referral')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.Unit')),
            ],
        ),
    ]
