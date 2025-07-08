from django.urls import path
from . import views

urlpatterns = [
    path('', views.DrinkList.as_view()),
    path('<int:pk>/', views.DrinkDetail.as_view()),
]