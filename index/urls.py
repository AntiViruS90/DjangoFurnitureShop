from django.urls import path, re_path, include
# from django.conf.urls import url

from . import views
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    CartView, CheckoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    path('', ProductListView.as_view(), name='product_list'),
    path('product_detail/<pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/comment', views.comment, name='comment'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('edit_product/<pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('product_detail/<pk>/delete_product/', ProductDeleteView.as_view(), name='delete_product'),
    path('add_to_cart/<pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_product_from_cart/<pk>/', views.remove_single_product_from_cart,
         name='remove_single_product_from_cart'),
    path('email/', CheckoutView.as_view(), name='email'),
    path('contacts/', views.contacts, name='contacts'),
    # path('<int:id>', views.product_list, name=''),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Create your tests here.  
 