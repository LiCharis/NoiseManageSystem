from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from car.models import Car
from clarity.models import Clarity
from loudness.models import Loudness
from sharpness.models import Sharpness
from volatility.models import Volatility


class Data(models.Model):

    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='汽车品牌')
    # clarity = models.ForeignKey(Clarity, on_delete=models.CASCADE, verbose_name='语音清晰度', default="")
    # loudness = models.ForeignKey(Loudness, on_delete=models.CASCADE, verbose_name='响度')
    # sharpness = models.ForeignKey(Sharpness, on_delete=models.CASCADE, verbose_name='尖锐度')
    # volatility = models.ForeignKey(Volatility, on_delete=models.CASCADE, verbose_name='波动度')
    speed = models.CharField(verbose_name='速度形式', max_length=50)
    condition = models.CharField(verbose_name='工况', max_length=100)
    status = models.CharField(verbose_name='荷载状态', max_length=100)
    first_left = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（左侧）-SPL_L')
    first_right = models.FloatField(verbose_name='测量次数一AA-BB内最大声压级（右侧）-SPL_R')
    second_left = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（左侧）-SPL_L')
    second_right = models.FloatField(verbose_name='测量次数二AA-BB内最大声压级（右侧）-SPL_R')
    image = models.FileField(upload_to='upload_image', default=" ")

    result = models.FloatField(verbose_name='通过噪声最终结果')

    class Meta:
        verbose_name = 'data'
        db_table = 'data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s | %s |%s |%s ' % (self.car, self.speed, self.condition, self.status)
