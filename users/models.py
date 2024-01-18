from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ 유저 모델 정의"""
    mobile = models.CharField(max_length=20)
    email = models.EmailField()