from bookshelf.models import Book

# Retrieving the book instance

book = Book.objects.get(title="1984")

# Output

print(book.title, book.author, book.publication_year)

# Expected Output: 1984 George Orwell 1949
