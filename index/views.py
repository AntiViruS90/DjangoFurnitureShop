from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils import timezone
from .models import Product, Comment, Order, OrderProduct, UserAddress
from .forms import CommentForm, CheckoutForm, UserForm, ProductForm
from django.core.mail import EmailMessage
from . import generate_invoice
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.models import Group
import telebot as telebot

bot = telebot.TeleBot('6530095170:AAFod26fN1Aih5d3_jf7-ncF4U0Y1pZYa_g')


class ProductListView(ListView):
    model = Product
    paginate_by = 4

    def get_queryset(self):
        search_phrase = self.request.GET.get('search')
        # search_manufacturer = self.request.GET.get('search_manufacturer')
        if search_phrase == None:
            search_phrase = self.request.GET.get('search_manufacturer')
            if search_phrase == None:
                object_list = self.model.objects.all()
            elif search_phrase != '':
                object_list = self.model.objects.filter(
                    manufacturer_id__username__icontains=search_phrase)
            else:
                object_list = self.model.objects.all()
        elif search_phrase != '':
            object_list = self.model.objects.filter(
                name__icontains=search_phrase)
        else:
            object_list = self.model.objects.all()
        return object_list


class ProductDetailView(LoginRequiredMixin, View):
    template_name = 'index/product_detail.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = Comment.objects.filter(product=product)
        comment_form = CommentForm()

        context = {'product': product, 'comments': comments, 'comment_form': comment_form}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()

        return redirect('product_detail', pk=pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'index/new_product.html'
    success_url = '?success'

    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.manufacturer = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'index/edit_product.html'

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.instance.manufacturer = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'index/cart.html', {'order': order})
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have an active order!")
            return redirect("/")


def send_order_notification_to_manufacturer(order):
    manufacturer_group = Group.objects.get(name='Provider')
    manufacturers = manufacturer_group.user_set.all()

    products_ordered = order.products.all()

    for manufacturer in manufacturers:
        product_info = []
        for product in products_ordered:
            product_info.append(f'{product.product.name} - Quantity: {product.quantity}')

        email = EmailMessage(
            'New Order Notification',
            f'A new order has been placed with the following products:\n{", ".join(product_info)}\n\n'
            f'Total number of products: {sum(product.quantity for product in products_ordered)}\n'
            f'Shipping Address: '
            f'{order.shipping_address.city, order.shipping_address.name, order.shipping_address.surname, order.shipping_address.street, order.shipping_address.house_number}\n',
            'slava90nikitin90@gmail.com',
            [manufacturer.email]
        )
        email.send()


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            shipping_address_qs = UserAddress.objects.filter(
                user=self.request.user,
            )
            if shipping_address_qs.exists():
                form = CheckoutForm(initial={
                    'company_name': shipping_address_qs[0].company_name,
                    'name': shipping_address_qs[0].name,
                    'surname': shipping_address_qs[0].surname,
                    'street': shipping_address_qs[0].street,
                    'house_number': shipping_address_qs[0].house_number,
                    'house_unit_number': shipping_address_qs[0].house_unit_number,
                    'post_code': shipping_address_qs[0].post_code,
                    'city': shipping_address_qs[0].city
                })
            else:
                form = CheckoutForm()
            context = {
                'form': form,
                'order': order,
            }
            return render(self.request, "index/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You have no order!")
            return redirect('/')

    def post(self, *args, **kwargs):
        form = CheckoutForm(data=self.request.POST)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                company_name = form.cleaned_data.get('company_name')
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                street = form.cleaned_data.get('street')
                house_number = form.cleaned_data.get('house_number')
                house_unit_number = form.cleaned_data.get('house_unit_number')
                post_code = form.cleaned_data.get('post_code')
                city = form.cleaned_data.get('city')
                payment_deadline = form.cleaned_data.get('payment_deadline')

                shipping_address = UserAddress(
                    user=self.request.user,
                    company_name=company_name,
                    name=name,
                    surname=surname,
                    street=street,
                    house_number=house_number,
                    house_unit_number=house_unit_number,
                    post_code=post_code,
                    city=city
                )
                shipping_address.save()
                order_products = OrderProduct.objects.filter(
                    user=self.request.user, ordered=False
                )
                items_list = []
                for order_product in order_products:
                    order_product.ordered = True
                    order_product.save()
                    items_list.append(order_product.quantity)
                    items_list.append(order_product.product.price)
                    items_list.append(order_product.product.name)
                generate_invoice.create_invoice('Furniture City', 'st. Furniture, 77', 'FurnitureTown',
                                                f'{shipping_address.name} {shipping_address.surname}',
                                                f'{shipping_address.street} {shipping_address.house_number}',
                                                shipping_address.post_code, items_list)
                order.shipping_address = shipping_address
                order.ordered = True
                order.payment_deadline = payment_deadline
                # print(f"{order.get_total()}")
                email = EmailMessage(
                    'Order confirmation',
                    f''' This is an automatically generated message.
                    DO NOT REPLY TO THE MESSAGE YOU RECEIVED.

                    Thank you for your order.
                    The order value is: $ {order.get_total()}.
                    The order must be paid by: {payment_deadline}
                    Otherwise, the order will be canceled.
                    ''', 'slava90nikitin90@gmail.com', [str(self.request.user.email)])
                email.attach_file('Proforma.pdf')
                email.send()
                order.save()

                # telegram bot
                chat_id = 682235838
                message = 'Name: ' + name + '\nSurname: ' + surname + "\nCity: " + city + \
                          '\nStreet: ' + street + '\nHouse number: ' + house_number
                items_list = str(items_list)
                print(items_list)
                answer = items_list + '\n' + message
                bot.send_message(chat_id, answer)

                send_order_notification_to_manufacturer(order)

                return render(self.request, "index/order_complete.html", {})
            else:
                print(form.errors)
                messages.info(
                    self.request, "Complete the required fields")
                return redirect("checkout")

        except ObjectDoesNotExist:
            messages.warning(
                self.request, "You do not have any active order")
            return redirect("cart")


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product.quantity += 1
            order_product.save()
            messages.info(request, "Quantity updated.")
            return redirect("cart")
        else:
            order.products.add(order_product)
            messages.info(request, "Added to cart.")
            return redirect("cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
        messages.info(request, "Added to cart.")
        return redirect('cart')


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product = OrderProduct.objects.filter(
                product=product, user=request.user, ordered=False)[0]
            order.products.remove(order_product)
            order_product.delete()
            messages.info(request, 'Product removed from cart')
            return redirect('cart')
        else:
            messages.info(request, 'Cart is empty')
            return redirect('product_detail', pk=pk)
    else:
        messages.info(request, 'Cart is empty')
        return redirect('product_detail', pk=pk)


@login_required
def remove_single_product_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_product_qs = OrderProduct.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )
            if order_product_qs.exists():
                order_product = order_product_qs[0]

                if order_product.quantity > 1:
                    order_product.quantity -= 1
                    order_product.save()
                else:
                    order.products.remove(order_product)
                    order_product.delete()
                messages.info(request, 'Quantity updated.')
                return redirect('cart')
            else:
                messages.info(request, 'This product is not in your cart')
                return redirect('product_detail', pk=pk)
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('product_detail', pk=pk)
    else:
        messages.info(request, 'You have no order')
        return redirect('product_detail', pk=pk)


def contacts(request):
    return render(request, 'index/contacts.html')


def error_404(request, exception):
    return render(request, 'index/404.html', status=404)


def FAQs(request):
    return render(request, 'index/FAQs.html')


@login_required
def cabinet(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('cabinet')
    else:
        form = UserForm(instance=user)
        user_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
    return render(request, 'index/cabinet.html', {'form': form, 'user_data': user_data})
