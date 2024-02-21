from django import forms
from django.contrib.auth.models import User
from .models import Product, Comment, UserAddress, Attachment
import datetime
from multiupload.fields import MultiFileField


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photo']  # not attachments!

    additional_photos = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ProductForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ProductForm, self).save(commit=False)
        instance.mafacturer = self.request.user

        if commit:
            instance.save()

        for each in self.cleaned_data['additional_photos']:
            Attachment.objects.create(additional_photos=each, product=instance)

        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
