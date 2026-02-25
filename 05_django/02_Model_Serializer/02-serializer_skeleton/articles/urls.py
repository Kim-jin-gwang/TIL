from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list_or_create),
    # 상세 조회, 수정, 삭제
    path('<int:article_pk>/', views.article_detail)
]