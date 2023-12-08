
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    
    first_name = None  # 查看AbstractUser继承的字段，将不需要的设置none
    last_name = None
    #email = None
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    name = models.CharField(verbose_name='姓名', max_length=50)
    agency = models.CharField(verbose_name='单位', max_length=50)
    department = models.CharField(verbose_name='部门', max_length=50)

    class Meta:
        verbose_name = '用户信息'
        db_table = 'user'
        verbose_name_plural = verbose_name

