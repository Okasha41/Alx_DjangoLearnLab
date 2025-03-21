from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# this serializer class returns the data of a book and validates it's publication year


class BookSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if int(data['publication_year']) > datetime.now().year:
            raise serializers.ValidationError(
                'Publication Year can not be in the future')

    class Mete:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']


# this serializer class return the data of author with all his related books
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
