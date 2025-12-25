from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser, Task

# Task forms (existing - keep these)
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']

# Authentication forms (NEW)
class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label="Password (for confirmation)",
        widget=forms.PasswordInput
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age', 'password1', 'password2')
        labels = {
            'username': 'username',
            'email': 'Email address',
            'age': 'age',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'user@example.com'})
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        # Check if password is only numbers
        if password1.isdigit():
            raise ValidationError("The password cannot contain only numbers.")
        
        # Check if password is too similar to personal info
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        
        if username and username.lower() in password1.lower():
            raise ValidationError("Password cannot be similar to your username.")
        
        if email:
            email_local = email.split('@')[0]
            if email_local.lower() in password1.lower():
                raise ValidationError("Password cannot be similar to your email.")
        
        return password2


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'age')
        labels = {
            'username': 'username',
            'email': 'Email address',
            'age': 'age',
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Original Password",
        widget=forms.PasswordInput
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    new_password2 = forms.CharField(
        label="New Password (for confirmation)",
        widget=forms.PasswordInput
    )
    
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        
        # Check if password is only numbers
        if password1.isdigit():
            raise ValidationError("The password cannot contain only numbers.")
        
        # Check similarity with user info
        user = self.user
        if user.username.lower() in password1.lower():
            raise ValidationError("Password cannot be similar to your username.")
        
        email_local = user.email.split('@')[0].lower()
        if email_local in password1.lower():
            raise ValidationError("Password cannot be similar to your email.")
        
        return password2
