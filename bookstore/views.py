from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, request


# Create your views here.
# user => urls => views => templetes
#                 views => model
#               
# view responsible for rendering templates
from .models import *
from .forms import Orderform ,CreateNewUser, ProfileInfo
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate ,login ,logout

from django.contrib.auth.decorators import login_required
from .decorators import notloggedUsers, allowedUsers, forAdmins
# when i create user it directly become customer
from django.contrib.auth.models import Group
# from django.forms import inlineformset_factory



# @allowedUsers(allowedGroups=['admin'])
@forAdmins    
@login_required(login_url='login')
def dashboard(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progres').count()
    out_orders = orders.filter(status='Out of order').count()
    # use context to return more than one objects
    context = {'customers' : customers ,
               'orders' : orders, 
                't_orders' : t_orders, 
                'p_orders' : p_orders, 
                'd_orders' : d_orders, 
                'in_orders' : in_orders, 
                'out_orders' : out_orders 
              }
    return render(request , 'bookstore-templates/dashboard.html', context)


@login_required(login_url='login')
def contacts(request):
    return render(request,'bookstore-templates/contacts.html')

@forAdmins 
@login_required(login_url='login')
def books(request):
    # take data from database from model <<books_model>> then send it to templates by name as <<books_template>>
    book = Book.objects.all() 

    context ={
          'books': books,
    } 
    return render(request,'bookstore-templates/books.html',context )


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def customer(request,pk):
    # use get instead of all because we need only one cutomer that match with the id
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()  
    order_count = orders.count()
    filter = OrderFilter(request.GET, queryset=orders )
    orders = filter.qs
    context = {'customers' : customers,
                'orders' : orders, 
                'order_count' : order_count,
                'filter' : filter, 
              }
    return render(request,'bookstore-templates/customer.html', context) 


@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request):
    # orderFormSet = inlineformset_factory(Customer, Order, fields=('book', 'status'))
    form = Orderform() 
    if request.method == 'POST':
        # print(request.POST) 
        form = Orderform(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form }
    return render(request,'bookstore-templates/order-form.html', context)   


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin-group']) 
def update(request,pk):
    order = Order.objects.get(id=pk)
    form = Orderform(instance=order) 
    if request.method == 'POST':
        form = Orderform(request.POST, instance=order)  
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form }
    return render(request,'bookstore-templates/order-form.html', context)   


@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin']) 
def delete(request,pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
            order.delete()
       
            return redirect('home')
    context = {'order': order }
    return render(request,'bookstore-templates/delete-form.html', context)  

# 3mlt form law7dha fel forms .py
    # form = UserCreationForm(request.POST)
    # if form.is_valid():
    #     form.save()

def reg(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
        form = CreateNewUser()
        if request.method == 'POST':
            form = CreateNewUser(request.POST)  
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                # make user a customer directly
                group = Group.objects.get(name ='customer')
                user.groups.add(group)
                messages.success(request, username + 'Created successfully')
                return redirect('login')

        context = {'form' : form}
        return render(request,'bookstore-templates/reg.html', context) 



# @login_required(login_url='login')
# def login(request):
#     return render(request,'bookstore-templates/login.html')


@notloggedUsers
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')

    context = {}
    return render(request,'bookstore-templates/login.html', context)    




def userLogout(request):
    logout(request)
    return redirect('login')  


# @notloggedUsers


# @login_required(login_url='login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):

    orders = request.user.customer.order_set.all()
    t_orders = orders.count()
    p_orders = orders.filter(status='Pending').count()
    d_orders = orders.filter(status='Delivered').count()
    in_orders = orders.filter(status='in progres').count()
    out_orders = orders.filter(status='Out of order').count()

    context = {
               'orders' : orders, 
                't_orders' : t_orders, 
                'p_orders' : p_orders, 
                'd_orders' : d_orders, 
                'in_orders' : in_orders, 
                'out_orders' : out_orders 
              }

    return render(request,'bookstore-templates/userProfile.html',context)   
           

# def index(request):
#     return render(request,'bookstore-templates/index.html')     



# @login_required(login_url='login')

def profileInfo(request):
    customer = request.user.customer
    form = ProfileInfo(instance=customer)



    if request.method == 'POST':
            form = ProfileInfo(request.POST, request.FILES, instance=customer)  
            if form.is_valid():
                form.save()

    context = {'form' : form}

    return render(request,'bookstore-templates/profileInfo.html',context)

