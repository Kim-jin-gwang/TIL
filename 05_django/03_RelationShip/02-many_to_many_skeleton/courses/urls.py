from django.urls import path
from . import views


urlpatterns = [
    path("<int:teacher_pk>/", views.create_course), 
    path("<int:teacher_pk>/assistant/<int:course_pk>/", views.assistant),  
 
]