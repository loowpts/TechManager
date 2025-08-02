from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department']
        labels = {
            'department': 'Отдел',
        }
