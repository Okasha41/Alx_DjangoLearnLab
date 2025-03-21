# api/test_views.py
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Book, Author
from api.serializers import BookSerializer


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints
    """

    def setUp(self):
        """Set up test data and authentication"""
        # Create users for permission testing
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )

        # Create test authors
        self.author1 = Author.objects.create(name="Test Author 1")
        self.author2 = Author.objects.create(name="Test Author 2")

        # Create test books
        self.book1 = Book.objects.create(
            title="Python Programming",
            author=self.author1,
            publication_year=2023,
            isbn="9781234567890"
        )

        self.book2 = Book.objects.create(
            title="Django for Beginners",
            author=self.author1,
            publication_year=2024,
            isbn="9789876543210"
        )

        self.book3 = Book.objects.create(
            title="Advanced REST APIs",
            author=self.author2,
            publication_year=2025,
            isbn="9785432109876"
        )

        # API endpoints
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})

        # Set up API client
        self.client = APIClient()

        # Data for creating and updating books
        self.valid_payload = {
            'title': 'New Test Book',
            'author': self.author2.id,
            'publication_year': 2025,
            'isbn': '9780123456789'
        }

        self.invalid_payload = {
            'title': '',
            'author': self.author1.id,
            'publication_year': 2030,  # Future year
            'isbn': 'invalid-isbn'
        }

    def test_get_all_books_unauthenticated(self):
        """Test retrieving all books without authentication"""
        response = self.client.get(self.list_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, serializer.data)

    def test_get_valid_single_book(self):
        """Test retrieving a valid single book"""
        response = self.client.get(self.detail_url)
        book = Book.objects.get(pk=self.book1.pk)
        serializer = BookSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_invalid_single_book(self):
        """Test retrieving an invalid book"""
        invalid_detail_url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(invalid_detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_unauthenticated(self):
        """Test creating a new book without authentication"""
        response = self.client.post(
            self.list_url, self.valid_payload, format='json')

        # Assuming your API requires authentication for POST requests
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Test creating a new book with authentication"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(
            self.list_url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.get(
            isbn='9780123456789').title, 'New Test Book')

    def test_create_invalid_book(self):
        """Test creating a new book with invalid data"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(
            self.list_url, self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book(self):
        """Test updating an existing book"""
        self.client.force_authenticate(user=self.admin_user)
        updated_data = {
            'title': 'Updated Python Book',
            'author': self.author1.id,
            'publication_year': 2024,
            'isbn': '9781234567890'
        }
        response = self.client.put(
            self.detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Python Book')

    def test_partial_update_book(self):
        """Test partially updating an existing book"""
        self.client.force_authenticate(user=self.regular_user)
        partial_data = {'title': 'Partially Updated Book'}
        response = self.client.patch(
            self.detail_url, partial_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Book')

    def test_delete_book_unauthorized(self):
        """Test regular user cannot delete a book"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.detail_url)

        # Assuming only admin users can delete books
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 3)

    def test_delete_book_authorized(self):
        """Test admin user can delete a book"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_filter_books_by_author(self):
        """Test filtering books by author"""
        url = f"{self.list_url}?author={self.author1.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only books by author1

    def test_filter_books_by_year(self):
        """Test filtering books by publication year"""
        url = f"{self.list_url}?publication_year=2025"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only books from 2025

    def test_search_books(self):
        """Test searching books by title"""
        url = f"{self.list_url}?search=Django"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_ordering_books(self):
        """Test ordering books by title"""
        url = f"{self.list_url}?ordering=title"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Alphabetically first
        self.assertEqual(response.data[0]['title'], 'Advanced REST APIs')

        # Test reverse ordering
        url = f"{self.list_url}?ordering=-title"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Alphabetically last
        self.assertEqual(response.data[0]['title'], 'Python Programming')
