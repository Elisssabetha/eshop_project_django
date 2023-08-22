from django import forms

from catalog.forms import StyleFormMixin
from mailing.models import MailingSettings, Customer, Message


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('start_time', 'end_time', 'period', 'status', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:MM:SS'
        self.fields['end_time'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:MM:SS'
class CustomerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('email', 'first_name', 'last_name', 'comment')


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'body')


class MailingSettingsForManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('status',)