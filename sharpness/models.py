from django.db import models

# Create your models here.
from car.models import Car
from total.models import Total


class Sharpness(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    total = models.ForeignKey(Total, on_delete=models.CASCADE, verbose_name='结果总表', null=True, blank=True)
    class Meta:
        verbose_name = '尖锐度数据'
        db_table = 'sharpness'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '左耳: %s |  右耳: %s|  尖锐度: %s' % (self.total.sharpness_left, self.total.sharpness_right, self.total.sharpness_result)
