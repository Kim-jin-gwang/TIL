from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.recommend_books),
    path('books/', views.book_list)
]