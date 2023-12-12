from django.db import models

# Create your models here.
from car.models import Car
from clarity.models import Clarity
from loudness.models import Loudness
from sharpness.models import Sharpness
from total.models import Total
from volatility.models import Volatility


class Data(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)
    total = models.ForeignKey(Total, on_delete=models.CASCADE, verbose_name='结果总表', null=True, blank=True)
    class Meta:
        verbose_name = '声压级结果'
        db_table = 'data'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s | %s |%s |%s ' % (self.total.speed, self.total.condition, self.total.status, self.total.data_result)
