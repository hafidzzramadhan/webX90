from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SystemImplementation

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SystemImplementationForm(forms.ModelForm):
    class Meta:
        model = SystemImplementation
        fields = ['no', 'nama_model', 'status_project', 'dokumentasi_model', 'laporan_model']