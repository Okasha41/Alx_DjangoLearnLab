from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.list_books, name='list_all_books'),
    path('library/<int:pk>', views.LibraryDetailView.as_view(),
         name='library_detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register')
]
