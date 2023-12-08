from django.db import models
# Create your models here.
from car.models import Car


class Clarity(models.Model):
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='汽车品牌')
    speed = models.CharField(verbose_name='速度形式', max_length=50, null=True, blank=True)
    condition = models.CharField(verbose_name='工况', max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name='荷载状态', max_length=100, null=True, blank=True)
    left = models.FloatField(verbose_name='语音清晰度度左耳-%', null=True, blank=True)
    right = models.FloatField(verbose_name='语音清晰度度右耳-%', null=True, blank=True)
    image = models.FileField(upload_to='upload_image', default=" ")

    class Meta:
        verbose_name = '语言清晰度数据'
        db_table = 'clarity'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '左耳: %s |  右耳: %s' % (self.left, self.right)
