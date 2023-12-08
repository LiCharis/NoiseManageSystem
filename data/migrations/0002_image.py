# Generated by Django 4.0.5 on 2023-09-19 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('file_name', models.CharField(max_length=200, verbose_name='图片名')),
                ('file_url', models.CharField(max_length=250, verbose_name='图片URL')),
            ],
            options={
                'verbose_name': 'images',
                'verbose_name_plural': 'images',
                'db_table': 'images',
            },
        ),
    ]
