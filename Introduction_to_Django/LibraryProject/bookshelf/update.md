from bookshelf.models import Book

# Retrieving the book instance

book = Book.objects.get(title="1984")

# Updating the title

book.title = "Nineteen Eighty-Four"
book.save()

# Output

print(book.title)

# Expected Output: Nineteen Eighty-Four
