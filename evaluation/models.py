from django.db import models

# Create your models here.
from total.models import Total


class Evaluation(models.Model):

    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    total = models.ForeignKey(Total, on_delete=models.CASCADE, verbose_name='结果总表', null=True, blank=True)

    class Meta:
        verbose_name = '声品质综合评价指数'
        db_table = 'evaluation'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % (self.total.index)