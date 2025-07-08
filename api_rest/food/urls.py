from django.urls import path
from . import views

urlpatterns = [
    path('', views.FoodList.as_view()),
    path('<int:pk>/', views.FoodDetail.as_view()),
]