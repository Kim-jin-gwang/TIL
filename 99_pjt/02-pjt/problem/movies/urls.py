from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/reviews/', views.create_review),
    path('genres/', views.get_genres),
    path('reviews/', views.get_reviews),
    path('reviews/<int:review_id>/', views.review_detail),
]
