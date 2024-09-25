from django.contrib import admin

from .models import *


models = [Customer, Product, Order, OrderItem, Shipping]

for model in models:
    admin.site.register(model)
