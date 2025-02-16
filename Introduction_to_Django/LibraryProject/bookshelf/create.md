from myapp.models import Book

# Creating a book instance

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Output

print(book)

# Expected Output: <Book: 1984 by George Orwell (1949)>
