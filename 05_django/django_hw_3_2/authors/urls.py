from django.urls import path
from . import views

app_name = 'authors'
urlpatterns = [
    # 특정 저자의 pk를 경로 변수로 받음
    path('<int:author_pk>/', views.author_detail),
]