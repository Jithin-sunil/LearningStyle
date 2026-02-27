from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='guest_home'),
    path('about/', views.About, name='guest_about'),
    path('register/user/', views.UserRegister, name='guest_user_register'),
    path('register/trainer/', views.TrainerRegister, name='guest_trainer_register'),
    path('login/', views.Login, name='guest_login'),
]
