from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book, Author

# response.data


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title='book1', )
