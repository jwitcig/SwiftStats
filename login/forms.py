from django.contrib.auth.models import User
from django import forms
from django.forms import Form, ModelForm

class CreateUserForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

class LoginForm(Form):

    username = forms.CharField(label='username', required=True)
    password = forms.CharField(label='password', required=True)

    class Meta:
        fields = ('username', 'password',)
