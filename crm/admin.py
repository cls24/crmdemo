from django.contrib import admin
from crm import models
# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.CustomerLevel)
admin.site.register(models.CustomerType)
admin.site.register(models.CustomerOrderType)
admin.site.register(models.OrderStatus)
admin.site.register(models.ProductModel)
admin.site.register(models.Factory)