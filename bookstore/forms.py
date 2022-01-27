from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Customer, Order, User



# inner class to take from models as object
# (ModelForm) to inherit from ModelForm
class Orderform(ModelForm):
     class Meta:
         model = Order 
         fields = "__all__"


class CreateNewUser(UserCreationForm):
     class Meta:
         model = User 
         fields = ['username','email','password1','password2']


class ProfileInfo(ModelForm):
     class Meta:
         model = Customer 
         fields = "__all__"
         exclude =['user']