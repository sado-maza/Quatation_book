from django.contrib.auth import  logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from Users.forms import RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    extra_context = {'title': "Авторизация"}




def logout_user(request):
    logout(request)  # очищает сессию
    return redirect('/')  # перенаправляем на главную

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register.html'
    extra_context = {'title': 'Регестрация'}
    success_url = reverse_lazy('Users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/profile.html'
    form_class = ProfileUserForm
    extra_context = {"title": "Ваш профиль"}

    def get_success_url(self):
        return reverse_lazy('Users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("Users:password_change_done.html")
    template_name = "user/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}

