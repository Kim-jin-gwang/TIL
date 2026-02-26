from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Course
from teachers.models import Teacher
from .serializers import CourseSerializer

# Create your views here.

# 메인 강사 pk를 받아서 새로운 강좌를 생성
@api_view(["POST"])
def create_course(request, teacher_pk):
    teacher = get_object_or_404(Teacher, pk=teacher_pk)
    serializer = CourseSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(main_teacher=teacher)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(["GET", "PUT", "DELETE"])
def course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    if request.method == "GET":
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def assistant(request, course_pk, teacher_pk):
    course = get_object_or_404(Course, pk=course_pk)
    teacher = get_object_or_404(Teacher, pk=teacher_pk)

    '''exists vs in
        exists는 데이터베이스에서 해당 조건을 만족하는 레코드가 존재하는지 여부를 반환
        in은 파이썬의 리스트나 쿼리셋에서 특정 객체가 포함되어 있는지를 확인하는 연산자
        둘 중 어떤 것을 사용할지는 상황에 따라 다르지만, 
        일반적으로 exists는 데이터베이스에서 직접 조건을 확인하기 때문에 더 효율적일 수 있음
    '''
    # 이미 부강사로 지정되어 있는 경우
    # if teacher in course.assistant_teachers.all():
    if course.assistant_teachers.filter(pk=teacher_pk).exists():
         # 해당 강좌의 부강사에서 제외
        course.assistant_teachers.remove(teacher)
     # 부강사로 지정되어 있지 않은 경우
    else:
         # 해당 강좌의 부강사로 지정
        course.assistant_teachers.add(teacher)

    # 부강사 지정/해제 후 강좌 정보를 반환
    serializer = CourseSerializer(course)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
