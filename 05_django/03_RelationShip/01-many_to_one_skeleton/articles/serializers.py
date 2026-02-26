from rest_framework import serializers
from .models import Article, Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('created_at', 'updated_at',)


class ArticleSerializer(serializers.ModelSerializer):
    # 나를 참조하고 있는 댓글들은... comment_set 이라는 매니저를 통해서 얻음
    # 나를 참조하는 댓글들의 id와 content 정보를 반환
    class CommentForArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'content')
    # 어.. 댓글들은 0개 이상 (N개) -> 많네> 
    comment_set = CommentForArticleSerializer(many=True, read_only=True)

    # annotate한 필드 추가 정의
    num_of_comments = serializers.SerializerMethodField()

    def get_num_of_comments(self, obj):
        return obj.num_of_comments

    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # class ArticleForCommentSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Article
    #         fields = ('id', 'title', )
    # 기존에 있었던 필드를 이렇게 수정하는 경우,
    # 대상 필드가 읽기 전욕으로 만들기 위해서, Serializer로 인스턴스를 생성할때
    # 그때, 읽기 전용이라고 명시 해 두고, 아래의 read_only_fields는 주석처리
    # article = ArticleForCommentSerializer(read_only=True)
    article = ArticleSerializer(read_only=True)
    class Meta:
        model = Comment
        # 사용자가 적지 않을 article 필드도 요구함
        fields = '__all__'
        # 진짜 생략해버림 -> article 정보 반환안함
        # exclude = ('article', ) 
        # read_only_fields = ('article', )
