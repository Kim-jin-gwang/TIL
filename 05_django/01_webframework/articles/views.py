from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
# view 함수는 기본적으로 사용자의 요청에 만족하는 응답을 만들어 낼것
# 즉, 사용자가 어떤 요청을 보냈는지를 알고 있어야 함
# view함수는 항상 사용자의 요청 정보를 인자로 받음

# GET 방식으로 보낼 때에만 실행
@api_view(['GET'])
def index(request):
    print(dir(request))
    # json 형태의 데이터를 응답
    
    return JsonResponse ({"message" : "hello,world!"})

@api_view(['GET'])
def article_detail(request, article_id):
    return JsonResponse({"message": f"article_id: {article_id}"})