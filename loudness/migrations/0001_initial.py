# Generated by Django 4.0.5 on 2023-09-21 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loudness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('speed', models.CharField(max_length=50, verbose_name='速度形式')),
                ('condition', models.CharField(max_length=100, verbose_name='工况')),
                ('status', models.CharField(max_length=100, verbose_name='荷载状态')),
                ('left', models.FloatField(verbose_name='响度左耳-sone')),
                ('right', models.FloatField(verbose_name='响度右耳-sone')),
                ('image', models.FileField(default=' ', upload_to='upload_image')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car.car', verbose_name='汽车品牌')),
            ],
            options={
                'verbose_name': 'loudness',
                'verbose_name_plural': 'loudness',
                'db_table': 'loudness',
            },
        ),
    ]
