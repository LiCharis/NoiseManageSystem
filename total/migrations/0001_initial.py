# Generated by Django 4.0.5 on 2023-12-11 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0003_alter_car_options_alter_car_brand_alter_car_gear_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('speed', models.CharField(max_length=50, verbose_name='速度形式')),
                ('condition', models.CharField(max_length=100, verbose_name='工况')),
                ('status', models.CharField(max_length=100, verbose_name='荷载状态')),
                ('first_left', models.FloatField(blank=True, null=True, verbose_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L')),
                ('first_right', models.FloatField(blank=True, null=True, verbose_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R')),
                ('second_left', models.FloatField(blank=True, null=True, verbose_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L')),
                ('second_right', models.FloatField(blank=True, null=True, verbose_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R')),
                ('image', models.FileField(default=' ', upload_to='upload_image', verbose_name='图片地址')),
                ('result', models.FloatField(blank=True, null=True, verbose_name='通过噪声最终结果')),
                ('car', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='car.car', verbose_name='汽车')),
            ],
            options={
                'verbose_name': '结果总表',
                'verbose_name_plural': '结果总表',
                'db_table': 'total',
            },
        ),
    ]
