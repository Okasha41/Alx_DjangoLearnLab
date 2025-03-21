from django.db import models

# this model create a table in database for Author with the following fields:
# name and books for it's books


class Author(models.Model):
    name = models.CharField(max_length=255)

# this model creates a table in database for Books with the following fields:
# title, publication year, related author


class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')
