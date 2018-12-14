from django import forms
from django.conf import settings
from .models import Course,Department
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
YEAR = (
    ('1st', 'Firs Year'),
    ('2nd', 'Second Year'),
    ('3rd', 'Third Year'),
    ('4rt', 'Fourth Year'),
)
class UserLoginForm(forms.Form):
    """login page"""
    email    = forms.EmailField(label='Email Address',widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def save(self):
        data     = self.cleaned_data
        email    = data['email']
        password = data['password']
        user     = authenticate(email=email, password=password)

        return user

    def clean(self, *args, **kwargs):
        email = self.data.get("email")
        password = self.data.get("password")

        if email and password:
            user_qs = User.objects.filter(email=email)

            if user_qs.count()==1:
                user = user_qs.first()
            else:
                raise forms.ValidationError("This User Does Not Exist")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect Password")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
                
        return super(UserLoginForm, self).clean(*args, **kwargs)
        
class UserRegisterForm(forms.Form):
    """
    The form for the register page
    """
    email      = forms.EmailField(label='Email Address',widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    id_number  = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'placeholder': 'Student ID'}))
    first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Lastname'}))
    last_name  = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder': 'Firsname'}))
    course     = forms.ModelChoiceField(queryset=Course.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    Year       = forms.ChoiceField(choices=YEAR)
    password   = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    def save(self):
        data = self.cleaned_data

        user = User(
            email      = data['email'],
            id_number  = data['id_number'],
            first_name = data['first_name'],
            last_name  = data['last_name'],
            Year       = data['Year'],
            password   = data['password'],

        )
        user.set_password(user.password)
        user.save()

        return user

    def clean_username(self):
        username = self.data.get('username')
        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("This Fucking username has already been used")
        return username
        
    def clean_email(self):
        email = self.data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been used")

        return email

 
 