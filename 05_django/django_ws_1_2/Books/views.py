from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from books import books
import random

# Create your views here.
@api_view(['GET'])
def book_recommend(request):
    selected = random.choice(books)
    return JsonResponse(selected)