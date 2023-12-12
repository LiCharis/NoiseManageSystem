# Generated by Django 4.0.5 on 2023-12-12 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('total', '0004_rename_clarity_total_clarity_result_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('total', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='total.total', verbose_name='结果总表')),
            ],
            options={
                'verbose_name': '声品质综合评价指数',
                'verbose_name_plural': '声品质综合评价指数',
                'db_table': 'evaluation',
            },
        ),
    ]
