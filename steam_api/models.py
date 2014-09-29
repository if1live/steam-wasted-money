#-*- coding: utf-8 -*-

from django.db import models

class Product(models.Model):
    appid = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    creatd_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
