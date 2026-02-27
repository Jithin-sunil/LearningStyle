from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='user_home'),
    path('test/', views.LearningStyleTest, name='user_test'),
    path('result/', views.Result, name='user_result'),
    path('recommended/', views.RecommendedContent, name='user_recommended'),
    path('progress/', views.Progress, name='user_progress'),
    path('logout/', views.Logout, name='user_logout'),
]
