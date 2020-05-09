# Generated by Django 3.0.3 on 2020-05-09 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0014_auto_20200509_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadditionalactivity',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_activities', to='masterlist.Establishment'),
        ),
        migrations.AlterField(
            model_name='estproductline',
            name='establishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_lines', to='masterlist.Establishment'),
        ),
    ]
