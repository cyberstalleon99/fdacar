# Generated by Django 3.0.6 on 2020-08-05 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0014_auto_20200729_0946'),
        ('pms', '0003_auto_20200805_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAddress',
            fields=[
                ('address_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='masterlist.Address')),
            ],
            bases=('masterlist.address',),
        ),
        migrations.CreateModel(
            name='ProductEstablishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.ProductAddress')),
                ('lto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='masterlist.Lto')),
                ('primary_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masterlist.PrimaryActivity')),
                ('specific_activity', models.ManyToManyField(to='masterlist.SpecificActivity')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='pms.ProductEstablishment', verbose_name='Establishment'),
        ),
    ]