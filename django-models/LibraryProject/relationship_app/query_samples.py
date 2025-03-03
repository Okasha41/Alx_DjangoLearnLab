from .models import Book, Library, Librarian, Author


def get_all_books_by_author(author):
    books = Book.objects.filter(author=author)


def query_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()


def query_librarian_for_library(library):
    librarian = Librarian.objects.filter(library=library)
