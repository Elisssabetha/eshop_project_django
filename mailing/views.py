from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, TemplateView

from mailing.forms import MailingSettingsForm, CustomerForm, MessageForm, MailingSettingsForManagerForm
from mailing.models import Customer, MailingSettings, MailingClient, Message
from mailing_blog.models import MailingBlog


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_queryset(self):
        """Пользователь видит только свои рассылки"""
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_mailingsettings'):
            return queryset  # Если есть право доступа, то пользователь видит все рассылки
        return queryset.filter(owner=self.request.user)


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        """ У рассылки появляется 'owner' - авторизированный пользователь """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(UserPassesTestMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')
    permission_required = 'mailing.change_mailingsettings'

    def test_func(self):
        mailing = self.get_object()
        user = self.request.user
        if mailing.owner == user or user.is_superuser:
            self.form_class = MailingSettingsForm
        elif user.has_perm('mailing.set_status'):
            self.form_class = MailingSettingsForManagerForm
        return user.is_authenticated and (mailing.owner == user or user.has_perm('mailing.set_status'))


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        """ Проверка на то, что пользователь не может удалять чужую рассылку """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MailingClientsListView(LoginRequiredMixin, ListView):
    """Клиенты рассылки"""

    model = MailingClient

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(settings=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients'] = Customer.objects.filter(owner=self.request.user)
        context_data['mailing_pk'] = self.kwargs.get('pk')

        return context_data


# customer

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer

    def get_queryset(self):
        """Пользователь видит только своих клиентов"""
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_customer'):
            return queryset  # Если есть право доступа, то пользователь видит всех клиентов (у манагера нет)
        return queryset.filter(owner=self.request.user)


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('mailing:customers')

    def form_valid(self, form):
        """ У клиента появляется 'owner' - авторизированный пользователь """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    success_url = reverse_lazy('mailing:customers')

    def get_object(self, queryset=None):
        """ Проверка на то, что пользователь не может менять чужого клиента """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy('mailing:customers')

    def get_object(self, queryset=None):
        """ Проверка на то, что пользователь не может удалить чужого клиента """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


# message

class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        """Пользователь видит только свои сообщения"""
        queryset = super().get_queryset()
        if self.request.user.has_perm('mailing.view_message'):
            return queryset  # Если есть право доступа, то пользователь видит все сообщения
        return super().get_queryset().filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        """ У сообщения появляется 'owner' - авторизированный пользователь """
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        """ Проверка на то, что пользователь не может менять чужое сообщение """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:messages')

    def get_object(self, queryset=None):
        """ Проверка на то, что пользователь не может удалять чужое сообщение """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return self.object


def toggle_customer(request, pk, customer_pk):
    # удаление клиента из рассылки
    if MailingClient.objects.filter(client_id=customer_pk, settings_id=pk).exists():
        MailingClient.objects.filter(client_id=customer_pk, settings_id=pk).delete()
    # добавление в рассылку
    else:
        MailingClient.objects.create(client_id=customer_pk, settings_id=pk)

    return redirect(reverse('mailing:mailing_clients', args=[pk]))


class HomePageView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing'] = MailingSettings.objects.all().count()
        context_data['count_mailing_active'] = MailingSettings.objects.filter(
            status=MailingSettings.STATUS_STARTED).count()
        context_data['count_unique_customers'] = Customer.objects.distinct().count()
        context_data['mailing_blog'] = MailingBlog.objects.all()[:3]
        context_data['title'] = 'Главная страница рассылок'
        return context_data
