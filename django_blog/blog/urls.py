from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('posts', views.posts, name='posts'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile')
]
