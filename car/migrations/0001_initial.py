# Generated by Django 4.0.5 on 2023-09-15 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('model', models.CharField(max_length=50, verbose_name='车型')),
                ('brand', models.CharField(max_length=50, verbose_name='品牌')),
            ],
            options={
                'verbose_name': 'car',
                'verbose_name_plural': 'car',
                'db_table': 'car',
            },
        ),
    ]