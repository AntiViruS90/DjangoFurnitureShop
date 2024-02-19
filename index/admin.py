from django.contrib import admin
from .models import Product, Comment, Order, OrderProduct, UserAddress
from . import models

admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(UserAddress)


class AttachmentInline(admin.StackedInline):
    model = models.Attachment
    extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]
