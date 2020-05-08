# Generated by Django 3.0.3 on 2020-05-08 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('masterlist', '0007_auto_20200508_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='establishment',
            name='additional_activity',
        ),
        migrations.CreateModel(
            name='EstAdditionalActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masterlist.AdditionalActivity')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masterlist.Establishment')),
            ],
        ),
    ]
