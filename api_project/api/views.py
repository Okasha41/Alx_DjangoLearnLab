from django.shortcuts import render
from rest_framework import generics, viewsets, permissions
from .serializers import BookSerializer
from .models import Book


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    model = Book
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
