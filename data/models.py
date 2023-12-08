from django.db import models

# Create your models here.
from car.models import Car
from clarity.models import Clarity
from loudness.models import Loudness
from sharpness.models import Sharpness
from volatility.models import Volatility


class Data(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='汽车品牌', null=True, blank=True)
    speed = models.CharField(verbose_name='速度形式', max_length=50, null=True, blank=True)
    condition = models.CharField(verbose_name='工况', max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name='荷载状态', max_length=100, null=True, blank=True)
    first_left = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L', null=True, blank=True)
    first_right = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R', null=True, blank=True)
    second_left = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L', null=True, blank=True)
    second_right = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R', null=True, blank=True)
    image = models.FileField(upload_to='upload_image', default=" ")

    result = models.FloatField(verbose_name='通过噪声最终结果', null=True, blank=True)

    class Meta:
        verbose_name = '声压级结果'
        db_table = 'data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s | %s |%s |%s ' % (self.car, self.speed, self.condition, self.status)
