# Generated by Django 4.0.5 on 2023-12-11 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('total', '0003_remove_total_data_result_total_clarity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='total',
            old_name='clarity',
            new_name='clarity_result',
        ),
        migrations.RenameField(
            model_name='total',
            old_name='data',
            new_name='data_result',
        ),
        migrations.RenameField(
            model_name='total',
            old_name='loudness',
            new_name='loudness_result',
        ),
        migrations.RenameField(
            model_name='total',
            old_name='sharpness',
            new_name='sharpness_result',
        ),
        migrations.RenameField(
            model_name='total',
            old_name='volatility',
            new_name='volatility_result',
        ),
    ]