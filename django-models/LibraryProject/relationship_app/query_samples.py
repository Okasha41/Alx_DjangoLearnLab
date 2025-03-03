from .models import Book, Library, Librarian


def get_all_books_by_author(id):
    queryset = Book.objects.filter(author_id=id)


def list_all_books_in_library():
    queryset = Library.objects.prefetch_related(Book).all()


def get_librarian(id):
    queryset = Librarian.objects.filter(library_id=id)
