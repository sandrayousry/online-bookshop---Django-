from django.urls import path
from .import views



urlpatterns = [
    
    path('home', views.dashboard, name='home'),
    path('contacts', views.contacts , name='contacts'),
    # path('index', views.index),
    path('books', views.books, name='books'),
    path('customer<str:pk>', views.customer, name='customer'),
    path('create', views.create, name='create'),
    path('update<str:pk>', views.update, name='update'),
    path('delete<str:pk>', views.delete, name='delete'),
    path('login', views.userLogin, name='login'),
    path('reg', views.reg, name='reg'),
    path('logout', views.userLogout, name='logout'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('profileInfo', views.profileInfo, name='profileInfo'),
   
]