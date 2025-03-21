from django.test import TestCase
from .models import Book, Author


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title='book1', )
