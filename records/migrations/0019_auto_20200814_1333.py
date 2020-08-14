# Generated by Django 3.0.6 on 2020-08-14 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('records', '0018_inspector'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstInspector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='est_nspectors', to='records.Inspection')),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Inspector',
        ),
    ]
