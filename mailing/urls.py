from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import CustomerListView, CustomerUpdateView, CustomerDeleteView, \
    CustomerCreateView, MailingSettingsListView, MailingSettingsCreateView, MailingSettingsUpdateView, \
    MailingSettingsDeleteView, MailingClientsListView, toggle_customer, MessageListView, MessageUpdateView, \
    MessageDeleteView, MessageCreateView, HomePageView

app_name = MailingConfig.name

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/update/<int:pk>', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>', CustomerDeleteView.as_view(), name='customer_delete'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer_create'),

    path('', MailingSettingsListView.as_view(), name='mailing_list'),
    path('create/', MailingSettingsCreateView.as_view(), name='mailing_create'),
    path('update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='mailing_update'),
    path('delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='mailing_delete'),

    path('<int:pk>/clients/', MailingClientsListView.as_view(), name='mailing_clients'),
    path('<int:pk>/clients/add/<int:customer_pk>', toggle_customer, name='mailing_clients_toggle'),

    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('messages/delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),

    path('homepage/', cache_page(60)(HomePageView.as_view()), name='mailing_homepage')
]
