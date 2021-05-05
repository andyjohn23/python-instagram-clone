from django import forms
from .models import UserAccount, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.forms.widgets import TextInput


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, help_text='Required valid emailaddress')

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccount.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f'Email {email} is already in use!')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = UserAccount.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f'Username {username} is already in use!')


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('invalid login')


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(),
                            max_length=15, required=True)
    email = forms.CharField(widget=forms.TextInput(),
                            max_length=100, required=True)

    class Meta:
        model = UserAccount
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'input is-medium'}), max_length=150, required=False)

    class Meta:
        model = Profile
        fields = ['bio']
