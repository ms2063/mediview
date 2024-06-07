from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={'placeholder':'사용자명(3자리 이상)'},
        ),
        )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'placeholder':'비밀번호 (8자리 이상)'},
        ),
        )
    
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1', 'password2','first_name', 'last_name', 'email', 'status']
    