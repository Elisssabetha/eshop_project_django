from django.urls import path

from catalog.views import homepage, contacts, products

urlpatterns = [
    path('', homepage, name='homepage'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products, name='products')
]
