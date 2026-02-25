from django.contrib import admin
from .models import Article

# Register your models here.
# 관리자 페이지에 article 모델을 등록
# 관리자.사이트.등록(게시글 모델)
admin.site.register(Article)