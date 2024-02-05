from django.contrib import admin
from .models import Product, Comment, Order, OrderProduct, UserAddress

admin.site.register(Product)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(UserAddress)

# Register your models here.
 