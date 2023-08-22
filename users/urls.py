from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ActivateView, CustomPasswordResetView, \
    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, UserUpdateView, \
    generate_new_password

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name='activate'),

    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('genpassword/', generate_new_password, name='generate_new_password'),


    path('profile/', UserUpdateView.as_view(), name='profile')
]
