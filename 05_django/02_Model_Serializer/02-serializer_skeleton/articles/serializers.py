# 직렬화 과정을 모두 거치는 파일

from rest_framework import serializers
from .models import Article

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title',]

# 게시글 생성을 위한 Ser
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id',  'title', 'content',]


# 상세 조회를 위한 Ser
class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

#게시글 수정을 위한 Ser
class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ['created_at', ]
        