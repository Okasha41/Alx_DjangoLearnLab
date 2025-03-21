from django.urls import path
from . import views

urlpatterns = [
    path('/books/', views.ListView()),
    path('books/<int:pk>'), views.DetailView()
]
