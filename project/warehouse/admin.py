from django.contrib import admin
from .models import Company, Product, WarehouseManager, Warehouse, User, OrderProduct
# Register your models here.

admin.site.register(User)
admin.site.register(Warehouse)
admin.site.register(WarehouseManager)
admin.site.register(Company)
admin.site.register(Product)
admin.site.register(OrderProduct)
