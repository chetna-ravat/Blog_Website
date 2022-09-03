
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    # the default value of emailfield is true which means that user have to input value, 
    # it would not allow blank
    
    email = forms.EmailField()

    # class meta is an optional class in model class and 
    # is used for model fields like changing order options,verbose_name, and a lot of other options.
    # https://www.geeksforgeeks.org/meta-class-in-models-django/

    class Meta():
        model = User
        # This fields list decides order of item on registeration
        fields = [ "email", "username", "password1", "password2"]