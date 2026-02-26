from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import BookSerializer, BookListSerializer
from .models import Book

# Create your views here.
@api_view(['GET', 'POST'])
def book_create_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        for book in books:
            print(book.title)
            for genre in book.genres.all():
                print(genre.name)
                print(genre.books.all())
            print('==')
            
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        print(request.data)
        serializer = BookSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/detail.html', {'book': book})