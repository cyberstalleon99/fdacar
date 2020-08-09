# Generated by Django 3.0.6 on 2020-08-06 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pms', '0009_auto_20200806_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='inspector',
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pms.Product')),
            ],
        ),
    ]