from . import views


from django.urls import path

urlpatterns = [
    path("", views.product_list),
    path('<int:category_pk>/', views.product_create),
]