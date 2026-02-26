from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True) 
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def article_detail(request, article_pk):
    # article = Article.objects.get(pk=article_pk)
    # 1의 입장인 article은 본인을 `참조`하고 있는 댓글들을
        # `역참조` 할 수 있습니다. -> 매니저를 통해서
        # `역참조 매니저`는 단순히 objects 라는 형태의 이름이 아니라
        # 나를 참조하고 있는 모델명의 소문자 + _set 
        # 지금상황으로는 Comment 라는 모델의 소문자 comment_set
    # <QuerySet [<Comment: 댓글 생성>, <Comment: 두번째 댓글 생성>, <Comment: 세번째 댓글 생성>]>
    from django.db.models import Count
    article = Article.objects.annotate(num_of_comments=Count('comment')).get(
        pk=article_pk
    )
    print(article.comment_set.all())
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        # PUT과 PATCH는 둘 다 업데이트를 위한 메서드이지만, PUT은 전체 업데이트, PATCH는 일부 업데이트를 의미
        serializer = ArticleSerializer(instance=article, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # DB에 댓글 정보를 생성할 때, 
        # article FK 정보는 내가 직접 삽입 해 주자.
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# comment = Comment.objects.get(pk=1)
# # 여기서부터는 파이선 객체이기 때문에 가능한 행위
#     # 실제 db에는 article의 id만 저장됩니다.
# print(comment.article.title)