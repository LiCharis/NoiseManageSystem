from django.db import models

# Create your models here.
from car.models import Car


class Total(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='汽车', null=True, blank=True)
    speed = models.CharField(verbose_name='速度形式', max_length=50)
    condition = models.CharField(verbose_name='工况', max_length=100)
    status = models.CharField(verbose_name='荷载状态', max_length=100)
    first_left = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L', null=True, blank=True, default=0)
    first_right = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R', null=True, blank=True, default=0)
    second_left = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L', null=True, blank=True, default=0)
    second_right = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R', null=True, blank=True, default=0)
    data_result = models.FloatField(verbose_name='声压级最终结果', null=True, blank=True, default=0)
    data_image = models.FileField(upload_to='upload_image', verbose_name="声压级图片地址", default=" ")

    clarity_left = models.FloatField(verbose_name='语音清晰度左耳-%', null=True, blank=True, default=0)
    clarity_right = models.FloatField(verbose_name='语音清晰度右耳-%', null=True, blank=True, default=0)
    clarity_result = models.FloatField(verbose_name='语音清晰度-%', null=True, blank=True, default=0)
    clarity_image = models.FileField(upload_to='upload_image', verbose_name="语音清晰度图片地址", default=" ")

    loudness_left = models.FloatField(verbose_name='响度左耳-sone', null=True, blank=True, default=0)
    loudness_right = models.FloatField(verbose_name='响度右耳-sone', null=True, blank=True, default=0)
    loudness_result = models.FloatField(verbose_name='响度-sone', null=True, blank=True, default=0)
    loudness_image = models.FileField(upload_to='upload_image', verbose_name="响度图片地址", default=" ")

    sharpness_left = models.FloatField(verbose_name='尖锐度左耳-acum', default=0)
    sharpness_right = models.FloatField(verbose_name='尖锐度右耳-acum', default=0)
    sharpness_result = models.FloatField(verbose_name='尖锐度-acum', null=True, blank=True, default=0)
    sharpness_image = models.FileField(upload_to='upload_image', verbose_name="尖锐度图片地址", default=" ")

    volatility_left = models.FloatField(verbose_name='波动度左耳-vacil', default=0)
    volatility_right = models.FloatField(verbose_name='波动度右耳-vacil', default=0)
    volatility_result = models.FloatField(verbose_name='波动度-vacil', default=0)
    volatility_image = models.FileField(upload_to='upload_image', verbose_name="波动度图片地址", default=" ")

    index = models.FloatField(verbose_name='声品质综合评价指数', default=0)

    class Meta:
        verbose_name = '结果总表'
        db_table = 'total'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s %s %s %s' % (self.id, self.car, self.speed, self.condition, self.status)
