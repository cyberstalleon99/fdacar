# Generated by Django 3.0.6 on 2020-08-06 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pms', '0006_auto_20200806_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_exiry',
            field=models.DateField(blank=True, null=True, verbose_name='Expiration Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_forwarded',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_manufactured',
            field=models.DateField(blank=True, null=True, verbose_name='Manufacuring Date'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_result_received',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='or_number',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='OR Number'),
        ),
        migrations.AlterField(
            model_name='product',
            name='remarks',
            field=models.TextField(blank=True, null=True, verbose_name='Remarks'),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pms.Unit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit_cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
