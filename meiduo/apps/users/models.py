from django.db import models

# Create your models here
# class User(models.Model):
#     username = models.CharField(max_length=20,unique=True),
#     password = models.CharField(max_length=20),
#     mobile = models.CharField(max_length=11,unique=True)

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True)
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    class Meta:
        db_table='tb_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name
