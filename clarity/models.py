from django.db import models
# Create your models here.
from car.models import Car
from total.models import Total


class Clarity(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    total = models.ForeignKey(Total, on_delete=models.CASCADE, verbose_name='结果总表', null=True, blank=True)
    class Meta:
        verbose_name = '语言清晰度数据'
        db_table = 'clarity'
        verbose_name_plural = verbose_name

    # def __str__(self):
    #     return '左耳: %s |  右耳: %s|  语言清晰度: %s' % (self.total.clarity_left, self.total.clarity_right, self.total.clarity)
