# Generated by Django 3.0.6 on 2020-07-28 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incoming', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Courier Name')),
            ],
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.DateField(verbose_name='Group')),
                ('dtn', models.CharField(max_length=14, verbose_name='DTN')),
                ('particulars', models.TextField()),
                ('remarks', models.TextField()),
                ('courier_tracking_number', models.CharField(max_length=250, verbose_name='Courier Tracking No.')),
                ('date_forwarded', models.DateField(verbose_name='Date Forwarded/Mailed')),
                ('forwarded_to', models.CharField(max_length=250, verbose_name='Forwarded To')),
                ('forwarded_to_1', models.CharField(max_length=250, verbose_name='Forwarded To (Company/Office Name)')),
                ('courier', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='outgoing.Courier', verbose_name='Courier Name')),
                ('document_type', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='incoming.DocumentType', verbose_name='Type of Document')),
                ('forwarded_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]