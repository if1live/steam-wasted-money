#-*- coding: utf-8 -*-

from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('appid', 'name', 'price')
    search_fields = ('appid',)

admin.site.register(Product, ProductAdmin)
