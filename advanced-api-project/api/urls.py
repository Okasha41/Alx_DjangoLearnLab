from django.urls import path
from . import views

urlpatterns = [
    path('/books/', views.ListView()),
    path('books/<int:pk>', views.DetailView()),
    path('/books/create/', views.CreateView()),
    path('/books/update/', views.UpdateView()),
    path('books/delete/', views.DeleteView())
]
