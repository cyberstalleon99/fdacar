# Generated by Django 3.0.2 on 2020-04-26 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='Clyde', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='Khayad', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='middle_initial',
            field=models.CharField(default='A', max_length=255),
            preserve_default=False,
        ),
    ]
