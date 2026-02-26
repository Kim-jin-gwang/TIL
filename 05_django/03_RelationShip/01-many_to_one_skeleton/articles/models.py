from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # article 클래스 변수에는 article 객체의 키값이 저장되길 바람.
    # 외래키를 저장 -> 누구의 외래키를 저장?
        # 반드시, 1: N의 관계에서는 N의 입장에 있는 객체는
        # 자신이 참조하고 있는 1의 입장의 객체가 삭제될때
        # 어떻게 처리할 것인지도 반드시 정의해야 한다.
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content