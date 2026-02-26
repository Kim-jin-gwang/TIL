from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializer import BookSerializer


# Create your views here.

@api_view(['GET', 'POST'])
def book_create_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)