# Generated by Django 4.0.5 on 2023-09-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loudness', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loudness',
            name='image',
            field=models.FileField(default='头像.jpg', upload_to='upload_image'),
        ),
    ]