from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='admin_home'),
    path('trainers/', views.ManageTrainers, name='admin_trainers'),
    path('topics/', views.Topics, name='admin_topics'),
    path('contents/', views.Contents, name='admin_contents'),
    path('assignments/', views.Assignments, name='admin_assignments'),
    path('reports/', views.Reports, name='admin_reports'),
    path('logout/', views.Logout, name='admin_logout'),
]
