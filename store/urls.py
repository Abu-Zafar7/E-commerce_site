from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('store/',views.store, name='store'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update_item/',views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('payment_success/',views.payment_success, name='payment_success'),
    path('order_complete/',views.order_complete, name='order_complete')
]