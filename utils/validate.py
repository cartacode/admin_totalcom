import re
from django import forms

def form_validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email) or ' ' in email:
        raise forms.ValidationError(u'Email is not valid.')

def form_validate_password(self, password):
    if len(password) < 8:
        self.add_error('password', u'Password should be 8 characters.')
    elif re.search('[0-9]',password) is None:
        self.add_error('password', u'Password should have at least one number.')
    elif re.search('[A-Z]',password) is None:
        self.add_error('password', u'Password should have at least one capital word.')
    else:
        pass

def form_validate_phone(phone_number):
    regex= "\w{3}-\w{3}-\w{4}"
    if not re.search(regex, phone_number):
        raise forms.ValidationError(u'Phone number is not valid.')