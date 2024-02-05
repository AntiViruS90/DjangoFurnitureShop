from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


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


class Comment(models.Model):
    post = models.ForeignKey('index.Product', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment = True
        self.save()


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
    login = models.CharField(max_length=10)
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
    house_number = models.CharField(max_length=30)
    house_unit_number = models.CharField(max_length=30, blank=True, null=True)
    post_code = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
