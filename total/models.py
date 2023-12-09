from django.db import models

# Create your models here.
from car.models import Car


class Total(models.Model):

    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='汽车品牌', null=True, blank=True)
    speed = models.CharField(verbose_name='速度形式', max_length=50)
    condition = models.CharField(verbose_name='工况', max_length=100)
    status = models.CharField(verbose_name='荷载状态', max_length=100)
    result = models.FloatField(verbose_name='声压级最终结果', null=True, blank=True)
    clarity_left = models.FloatField(verbose_name='语音清晰度左耳-%', null=True, blank=True)
    clarity_right = models.FloatField(verbose_name='语音清晰度右耳-%', null=True, blank=True)
    clarity = models.FloatField(verbose_name='语音清晰度-%', null=True, blank=True)
    loudness_left = models.FloatField(verbose_name='响度左耳-sone', null=True, blank=True)
    loudness_right = models.FloatField(verbose_name='响度右耳-sone', null=True, blank=True)
    loudness = models.FloatField(verbose_name='响度-sone', null=True, blank=True)
    sharpness_left = models.FloatField(verbose_name='尖锐度左耳-acum')
    sharpness_right = models.FloatField(verbose_name='尖锐度右耳-acum')
    sharpness = models.FloatField(verbose_name='尖锐度-acum', null=True, blank=True)
    volatility_left = models.FloatField(verbose_name='波动度左耳-vacil')
    volatility_right = models.FloatField(verbose_name='波动度右耳-vacil')
    volatility = models.FloatField(verbose_name='波动度-vacil')
    index = models.FloatField(verbose_name='声品质综合评价指数', default=0)

    class Meta:
        verbose_name = '结果总表'
        db_table = 'total'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % (self.index)