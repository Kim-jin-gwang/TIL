from rest_framework import serializers
from .models import Author

class AuthorDetailSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(source='books.count', read_only = True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']