from django.contrib import admin

from mailing.models import Customer, Message, MailingSettings, MailingClient, MailingLog


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'owner')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'owner')



@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'period', 'status', 'message', 'owner')


@admin.register(MailingClient)
class MailingClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'settings')


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'client', 'settings', 'status', 'server_response')

