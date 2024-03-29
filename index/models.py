from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission, User


class Product(models.Model):
    name = models.CharField(max_length=200)
    manufacturer = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField(max_length=800)
    created_date = models.DateTimeField(default=timezone.now)
    price = models.FloatField()
    photo = models.ImageField(upload_to='media/', null=True, blank=True)

    def __str__(self):
        return self.name

    def create(self):
        self.created_date = timezone.now()
        self.save()

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={
            'pk': self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={
            'pk': self.pk
        })

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    def average_rating(self):
        total_rating = sum(comment.rating for comment in self.comments.all())
        num_comments = self.comments.count()
        return total_rating / num_comments if num_comments else 0


class Attachment(models.Model):
    product = models.ForeignKey(Product, verbose_name=_('Product'), on_delete=models.CASCADE)
    additional_photos = models.FileField(_('Additional Photos'), upload_to='media/additional_photos')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.created_date}"


class OrderProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'UserAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    sale_date = models.DateField(auto_now_add=True)
    payment_deadline = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_price()
        return total


class User(models.Model):
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.CharField(max_length=30)


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    house_number = models.CharField(max_length=10)
    house_unit_number = models.CharField(max_length=10, blank=True, null=True)
    post_code = models.IntegerField()
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )

    def __str__(self):
        return self.username
