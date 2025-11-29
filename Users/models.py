from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    img = models.ImageField(upload_to="images/%Y/%m",default="img/defolt.png", verbose_name="Аватарка")
    sum_of_likes = models.IntegerField(default=0)
    sum_of_dislikes = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True,default="", verbose_name="Описание")

