from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# makemigration 3shan a7wlaha ll language tfhmha al database
#   a7wl al classes l tables fel django or lama a3ml t3delat
# migrate 3shan a3ml tables gwa al Database
# aro7 ll admin.py a3ml import lkol asmaa altabels 3shan ysm3o fel admin
# self m3naha an al function de tab3a ll class da


    # kol user hwa customer
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=190, null=True)
    email = models.CharField(max_length=190, null=True)
    phone = models.CharField(max_length=190, null=True)
    age = models.CharField(max_length=190, null=True)
    avatar = models.ImageField(blank = True, null=True, default='avatar.png') 
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__ (self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=190, null=True)
    def __str__ (self):
        return self.name

class Book(models.Model):
    CATEGORY= {
        ('Classic','Classic'),
        ('Comic','Comic'),
        ('Fantasy','Fantasy'),
        ('Horror','Horror')
    }
    name = models.CharField(max_length=190, null=True) 
    author =  models.CharField(max_length=190, null=True)
    url =  models.URLField(max_length=300, null=True)
    category =  models.CharField(max_length=190, null=True, choices=CATEGORY)
    description =  models.CharField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__ (self):
        return self.name




class Order(models.Model):
    STATUS= {
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('in progres','in progres'),
        ('Out of order','Out of order')
    }

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, null=True, on_delete=models.SET_NULL) 
    tag = models.ManyToManyField(Tag) 
    date_created = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    

    def __str__ (self):
        return self.customer    

