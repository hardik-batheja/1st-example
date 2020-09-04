
from django.urls import path, include
from basicapp import views

app_name = 'basicapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login', views.user_login, name='user_login'),
    path('view/', views.viewdb, name='view'),
    path('dbms/', views.dbms, name='dbms'),
    path('order/', views.createorder, name='order'),
]
