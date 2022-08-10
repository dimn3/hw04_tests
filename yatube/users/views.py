# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class PasswordChangeDone(TemplateView):
    template_name = 'users/password_change_done'


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(TemplateView):
    success_url = reverse_lazy('PasswordChangeDoneView')
    template_name = 'users/password_change_form.html'


class PasswordReset(TemplateView):
    success_url = reverse_lazy('PasswordResetConfirmView')
    template_name = 'users/password_reset_confirm.html'
