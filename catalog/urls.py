from django.urls import path

from catalog.views import homepage, contacts

urlpatterns = [
    path('', homepage, name='homepage'),
    path('contacts/', contacts, name='contacts'),
]
