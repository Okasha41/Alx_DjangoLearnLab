from .models import Book, Library, Librarian, Author


def get_all_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = author.books.all()


def query_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()


def query_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = library.librarian
