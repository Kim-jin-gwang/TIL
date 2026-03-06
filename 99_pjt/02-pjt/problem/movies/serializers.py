from rest_framework import serializers
from django.db.models import Avg, Count
from .models import Movie, Genre, Cast, Review
from accounts.models import User

class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'release_date', 'popularity', 'budget', 'revenue', 'runtime', 'genres']

    def get_genres(self, obj):
        return list(obj.genre_set.values_list('id', flat=True))

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('name', 'character', 'order')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('movie', )


class GenreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)
        
class MovieForReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', )

class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieForReviewSerializer(read_only=True)
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username')

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', )


class ReviewBriefSerializer(serializers.ModelSerializer):
    class AuthorSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('id', 'username')

    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('author', 'content', 'rating')

class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    vote_count = serializers.SerializerMethodField()
    genres = GenreNameSerializer(source='genre_set', many=True, read_only=True)
    cast_set = CastSerializer(source='casts', many=True, read_only=True)
    review_set = ReviewBriefSerializer(source='reviews', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'popularity', 'budget', 'revenue', 'runtime', 'average_rating', 'vote_count', 'genres', 'cast_set', 'review_set']

    def get_average_rating(self, obj):
        agg = obj.reviews.aggregate(avg=Avg('rating'))
        # return float average (or 0.0 if no ratings)
        return agg['avg'] if agg['avg'] is not None else 0.0

    def get_vote_count(self, obj):
        agg = obj.reviews.aggregate(count=Count('rating'))
        return agg['count']
