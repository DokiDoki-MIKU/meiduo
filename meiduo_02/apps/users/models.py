from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile=models.CharField(max_length=11,unique=True)

    class Meta:
        db_table='tb_users'
        verbose_name='用户管理'
        verbose_name_plural=verbose_name
