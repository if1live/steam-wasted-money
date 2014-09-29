#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('appid', 'name', 'price')

admin.site.register(Product, ProductAdmin)
