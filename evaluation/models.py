from django.db import models

# Create your models here.
class Evaluation(models.Model):

    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    brand = models.CharField(verbose_name='汽车品牌', max_length=50)
    speed = models.CharField(verbose_name='速度形式', max_length=50)
    condition = models.CharField(verbose_name='工况', max_length=100)
    status = models.CharField(verbose_name='荷载状态', max_length=100)
    index = models.FloatField(verbose_name='声品质综合评价指数', default=0)

    class Meta:
        verbose_name = '声品质综合评价指数'
        db_table = 'evaluation'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s%s' % (self.brand, self.index)