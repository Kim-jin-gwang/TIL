from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Author
from .serializer import AuthorDetailSerializer

@api_view(['GET'])
def author_detail(request, author_pk):
    author = get_object_or_404(Author, pk=author_pk)
    serializer = AuthorDetailSerializer(author)
    return Response(serializer.data)
