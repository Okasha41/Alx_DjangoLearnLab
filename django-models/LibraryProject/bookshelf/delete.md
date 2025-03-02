from bookshelf.models import Book

# Retrieving the book instance

book = Book.objects.get(title="Nineteen Eighty-Four")

# Deleting the book instance

book.delete()

# Output

print(Book.objects.all())

# Expected Output: <QuerySet []>
