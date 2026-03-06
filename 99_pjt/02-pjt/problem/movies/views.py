from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Genre, Review
from .serializers import MovieListSerializer, ReviewSerializer, MovieSerializer, GenreSerializer

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_review(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, author=request.user) # assign authenticated user as author
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_genres(request):
    data = get_list_or_404(Genre)
    serializer = GenreSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_reviews(request):
    data = get_list_or_404(Review)
    serializer = ReviewSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def review_detail(request, review_id):
    data = get_object_or_404(Review, pk=review_id)
    if request.method == 'GET':
        serializer = ReviewSerializer(data)
        return Response(serializer.data)
    elif data.author == request.user:
        if request.method == 'DELETE':
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == 'PUT' or request.method == 'PATCH':
            partial = request.method == 'PATCH'
            serializer = ReviewSerializer(data, data=request.data, partial=partial)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({'detail': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)