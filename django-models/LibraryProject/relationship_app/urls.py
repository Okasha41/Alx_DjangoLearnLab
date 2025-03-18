from django.urls import path
from . import views


urlpatterns = [
    path('books/', views.list_books, name='list_all_books'),
    path('library/<int:pk>', views.LibraryDetailView.as_view(),
         name='library_detail'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register.as_view(), name='register'),
    path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.librarian_view, name='librarian'),
    path('member/', views.member_view, name='member'),
]
