from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Product
from .serializer import ProductSerializer
from rest_framework.response import Response
from categories.models import Category
from django.shortcuts import get_object_or_404
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)


@api_view(['POST'])
def product_create(request, category_pk):
    category = get_object_or_404(Category, pk=category_pk)
    serializer = ProductSerializer(data = request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(category=category)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.erorrs, status=status.HTTP_400_BAD_REQUEST)
