from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleListSerializer, ArticleCreateSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def article_list_or_create(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # 게시글 생성
        serializer = ArticleCreateSerializer(data = request.data)

        # 사용자가 전송한 데이터가 DB에 삽입하기 적절한지 유효성 검사
            # is_valid = Bool
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        # return Response(serializer.errors)


@api_view(['GET', 'POST', 'DELETE'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET': pass
    elif request.method == 'POST': pass
    elif request.method == 'DELETE': pass