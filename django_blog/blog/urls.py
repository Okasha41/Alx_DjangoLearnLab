from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('posts', views.posts, name='posts'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.ListView.as_view(), name='list-view'),
    path('posts/new/', views.CreateView.as_view(), name='create-view'),
    path('posts/<int:pk>/', views.DetailView.as_view(), name='detail-view'),
    path('posts/<int:pk>/edit/', views.UpdateView.as_view(), name='update-view'),
    path('posts/<int:pk>/delete/', views.DeleteView.as_view(), name='delete-view'),
]
