from django.db import models

# Create your models here.
class Car(models.Model):

    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    model = models.CharField(verbose_name='车型', max_length=50)
    brand = models.CharField(verbose_name='品牌', max_length=50)

    class Meta:
        verbose_name = 'car'
        db_table = 'car'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s' % (self.brand)