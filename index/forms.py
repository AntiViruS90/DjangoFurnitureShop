from django import forms
from .models import Product, Comment, UserAddress, User
import datetime


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'photo')
        exclude = ('manufacturer', 'created_date',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')


class CheckoutForm(forms.Form):
    company_name = forms.CharField(max_length=20, required=False)
    name = forms.CharField(max_length=30)
    surname = forms.CharField(max_length=30)
    street = forms.CharField(max_length=30)
    house_number = forms.CharField(max_length=30)
    house_unit_number = forms.CharField(max_length=30, required=False)
    post_code = forms.CharField(max_length=30)
    city = forms.CharField(max_length=30)
    payment_deadline = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = UserAddress
        fields = ('company_name', 'name', 'surname', 'street', 'house_number', 'house_unit_number', 'post_code', 'city')



from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', 'name', 'surname', 'email']
