from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='trainer_home'),
    path('learner/<int:user_id>/', views.LearnerDetail, name='trainer_learner_detail'),
    path('logout/', views.Logout, name='trainer_logout'),
]
