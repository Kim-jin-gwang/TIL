from django.db import models

# Create your models here.
class Article(models.Model): # models.Model을 상속받아 사용
    # 이 클래스 변수가 곧 테이블의 컬럼이 된다.
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 프린트 함수를 통해 출력했을 때, 보기 좋도록 정제된 값을 반환
    # self에는 인스턴스가 들어감
    def __str__(self):
        return self.title # 현재 조회 중인 객체의 제목 문자열이 들어감
    