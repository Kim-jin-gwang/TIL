from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

menus = [
    {"name": "Espresso", "price": 3000},
    {"name": "Americano", "price": 3500},
    {"name": "Latte", "price": 4000}
]


@api_view(['GET'])
def menus_list(request):
    return Response(menus)