from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Product, Comment, Order, OrderProduct, UserAddress
from .forms import ProductForm, CommentForm, CheckoutForm
from django.core.mail import EmailMessage
from . import generate_invoice
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View


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


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'index/new_product.html'
    fields = ['name', 'description', 'price', 'photo']

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.manufacturer = self.request.user
        obj.save()
        return redirect('/')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'index/edit_product.html'
    fields = ['name', 'description', 'price', 'photo']


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
                email = EmailMessage('Order confirmation',
                                     f''' This is an automatically generated message.
                    DO NOT REPLY TO THE MESSAGE YOU RECEIVED.

                    Thank you for your order.
                    The order value is: $ {order.get_total()}.
                    The order must be paid by: {payment_deadline}
                    Otherwise, the order will be canceled.
                    ''', 'slava-nikitin-1990@mail.ru', [str(self.request.user.email)])
                email.attach_file('Proforma.pdf')
                email.send()
                order.save()
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

    # def bot_message(self, request):
    #     order_products = OrderProduct.objects.filter(user=self.request.user, ordered=False)
    #     form = CheckoutForm(data=self.request.POST)
    #     if request.POST:
    #         if form.is_valid():
    #             name = form.cleaned_data.get('name')
    #             surname = form.cleaned_data.get('surname')
    #             city = form.cleaned_data.get('city')
    #             street = form.cleaned_data.get('street')
    #             house_number = form.cleaned_data.get('house_number')
    #             # items = Cart.objects.filter(user_id=request.user.id)
    #             order = ''
    #             for one in order_products:
    #                 order += one.product.desription + ' ' + str(one.count) + 'шт. ' + str(one.total) + 'руб. ' + '\n'
    #             total = 0
    #             print(order)
    #             # for i in items:
    #             #     total += i.total
    #             # OrderCart.objects.create(address=address, name=name, tel=tel, total=total, order=order)
    #             # items.delete()
    #             ##########################################################################################
    #             token = '6530095170:AAFod26fN1Aih5d3_jf7-ncF4U0Y1pZYa_g'
    #             chat_id = 682235838  # 682235838
    #             message = order + '\nName: ' + name + '\nSurname: ' + surname + "\nCity: " + city + \
    #                       '\nStreet: ' + street + '\nHouse number: ' + house_number
    #             url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'
    #
    #             print(order)
    #             print(request)
    #             # print(requests.get(url).json())
    #             # return redirect('home')
    #             #     return HttpResponse('Data successfully')  # Вариант 1
    #             return JsonResponse({'message': 'Data successfully', 'link': '../'})
    #
    #     else:
    #         # Если запрос не POST, то просто отображаем страницу заказа
    #         return render(request, 'index/order_snippet.html')


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


# @login_required
# def remove_single_product_from_cart(request, pk):   #
#     product = get_object_or_404(Product, pk=pk)     #
#     order_qs = Order.objects.filter(        #
#         user=request.user,      #
#         ordered=False       #
#     )
#     if order_qs.exists():   #
#         order = order_qs[0] #
#         if order.products.filter(product__pk=product.pk).exists():  #
#             order_product = OrderProduct.objects.filter(    #   order_product_qs
#                 product=product,    #
#                 user=request.user,  #
#                 ordered=False       #
#             )[0]        #
#
#             if order_product.quantity > 1:
#                 order_product.quantity -= 1
#                 order_product.save()
#             else:
#                 order.products.remove(order_product)
#                 order_product.delete()
#             messages.info(request, 'Quantity updated.')
#             return redirect('cart')
#         else:
#             messages.info(request, 'This product is not in your cart')
#             return redirect('product_detail', pk=pk)
#     else:
#         messages.info(request, 'You have no order')
#         return redirect('product_detail', pk=pk)


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





@login_required
def comment(request, id):
    product_comment = get_object_or_404(Product, id=id)  # Product.objects.get(id=id)
    comments_all = Comment.objects.filter(post=product_comment,
                                          approved_comment=True)  # product_comment.comment_set.filter(active=True) models.py
    form_comment = CommentForm(request.POST)  # forms.py
    if request.POST and form_comment.is_valid():
        # if form.is_valid():
        comment_new = form_comment.save(commit=False)
        comment_new.post = product_comment
        comment_new.save()
        comment_new = Comment.objects.create()
        comment_new.author = request.POST.get('author')
        comment_new.post = request.POST.get('post')
        comment_new.approved_comment = product_comment
        comment_new.save()
        comment_mas = str(comment_new.textarea)
        my_mas = comment_mas.split()
        bad_words = ['ужасный', 'плохой', 'плохо', 'тварь', 'твари', 'кошмар', 'черт', 'bad']
        for element in my_mas:
            if element not in bad_words:
                comment_new.approved_comment = True
            else:
                comment_new.approved_comment = False
                break
        comment_new.save()
    else:
        form_comment = CommentForm()

    context = {'form_comment': form_comment, 'comments_all': comments_all}  # 'comment': product_comment
    return render(request, 'index/product_detail.html', context)


def contacts(request):
    return render(request, 'index/contacts.html')


"""
https://api.telegram.org/bot6530095170:AAFod26fN1Aih5d3_jf7-ncF4U0Y1pZYa_g
"""

@login_required
def bot_message(self, request):
    order_products = OrderProduct.objects.filter(user=self.request.user, ordered=False)
    form = CheckoutForm(data=self.request.POST)
    if request.POST:
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            city = form.cleaned_data.get('city')
            street = form.cleaned_data.get('street')
            house_number = form.cleaned_data.get('house_number')
            # items = Cart.objects.filter(user_id=request.user.id)
            order = ''
            for one in order_products:
                order += one.product.desription + ' ' + str(one.count) + 'шт. ' + str(one.total) + 'руб. ' + '\n'
            total = 0
            print(order)
            # for i in items:
            #     total += i.total
            # OrderCart.objects.create(address=address, name=name, tel=tel, total=total, order=order)
            # items.delete()
            ##########################################################################################
            token = '6530095170:AAFod26fN1Aih5d3_jf7-ncF4U0Y1pZYa_g'
            chat_id = 682235838  # 682235838
            message = order + '\nName: ' + name + '\nSurname: ' + surname + "\nCity: " + city + \
                      '\nStreet: ' + street + '\nHouse number: ' + house_number
            url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}'

            print(order)
            print(request)
            # print(requests.get(url).json())
            # return redirect('home')
            #     return HttpResponse('Data successfully')  # Вариант 1
            return JsonResponse({'message': 'Data successfully', 'link': '../'})

    else:
        # Если запрос не POST, то просто отображаем страницу заказа
        return render(request, 'index/order_snippet.html')


def error_404(request):
    return render(request, 'index/404.html')