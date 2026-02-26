
from django.urls import path
from . import views

urlpatterns = [
    path("",views.book_create_list),
]
