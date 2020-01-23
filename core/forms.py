# GlassFrogg/forms.py

from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from core.models import BaseUser
from utils.validate import form_validate_email, form_validate_password


class BaseSignupForm(ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"type": "text",
                                        "placeholder": "Username",
                                        "class": "form-control"}),
        required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "text",
                                        "placeholder": "Email",
                                        "class": "form-control"}),
        required=True)
    password = forms.CharField(
        widget=forms.TextInput(attrs={"type": "password",
                                        "placeholder": "Password",
                                        "class": "form-control"}),
        required=True)
    confirm_password = forms.CharField(
        widget=forms.TextInput(attrs={"type": "password",
                                        "placeholder": "Conform password",
                                        "class": "form-control"}),
        required=True)

    class Meta:
        model = BaseUser
        fields = ['username', 'email', 'password',]

    def clean_username(self):
        username = self.cleaned_data['username']
        if BaseUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        form_validate_email(email)
        if BaseUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(u'Email "%s" is already in use.' % email)
        return email

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        required_fields = []

        for field in required_fields:
            if not self.cleaned_data.get(field):
                self.add_error(field, u'"%s" shouldn\'t be empty' % field)

        form_validate_password(self, password)

        if password != confirm_password:
            self.add_error('confirm_password', u'Password is not matched.')

    def save(self, password=None):
        instance = super(BaseSignupForm, self).save()
        if password:
            instance.set_password(password)
        instance.username = instance.email
        instance.save()

        return instance


class BaseLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"type": "text",
                                        "placeholder": "Email",
                                        "class": "form-control"}),
        required=True)
    password = forms.CharField(
        widget=forms.TextInput(attrs={"type": "password",
                                        "placeholder": "Password",
                                        "class": "form-control"}),
        required=True)

    def clean(self):
        password = self.cleaned_data['password']
        form_validate_password(self, password)
