# Generated by Django 4.0.5 on 2023-09-20 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loudness', '0002_loudness_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loudness',
            name='image',
            field=models.FileField(default=' ', upload_to='upload_image'),
        ),
    ]