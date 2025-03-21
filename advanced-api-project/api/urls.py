from django.urls import path
from . import views

urlpatterns = [
    path('/books/', views.ListView.as_view()),
    path('books/<int:pk>', views.DetailView.as_view()),
    path('/books/create/', views.CreateView.as_view()),
    path('/books/update/', views.UpdateView.as_view()),
    path('books/delete/', views.DeleteView.as_view())
]
