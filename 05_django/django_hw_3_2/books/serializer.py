from rest_framework import serializers
from .models import Book
from authors.models import Author

class BookSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Author
            fields = '__all__'
            
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = '__all__'
