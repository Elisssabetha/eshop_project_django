from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.views import LogoutView as BaseLogoutView

from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView

from config import settings
from users.email_verification_token_generator import email_verification_token
from users.forms import UserRegisterForm, CustomPasswordResetForm, CustomResetConfirmForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        current_site = get_current_site(self.request)
        subject = 'Активация профиля'

        send_mail(
            subject=subject,
            message=f'Активируйте ваш профиль: http://{current_site.domain}/users/activate/{urlsafe_base64_encode(force_bytes(new_user.pk))}/{email_verification_token.make_token(new_user)}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)

    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class ActivateView(View):

    def get_user_from_email_verification_token(self, uid, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                get_user_model().DoesNotExist):
            return None

        if user is not None \
                and \
                email_verification_token.check_token(user, token):
            return user
        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    email_template_name = 'users/password_reset_email.html'
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def form_valid(self, form):
        # Метод, который отрабатывает при успешной валидации формы
        if form.is_valid():
            self.object = form.save()
            send_mail(
                subject='Изменения пароля',
                message=f'Вы поменяли пароль от своего профиля',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
        return super().form_valid(form)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    password = User.objects.make_random_password(length=10)
    request.user.set_password(password)
    request.user.save()

    send_mail(
        subject='Изменения пароля',
        message=f'Ваш новый пароль {password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('users:login'))
