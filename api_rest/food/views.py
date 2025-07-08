from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializer import FoodSerializer
from .models import Food

# Create your views here.
class FoodList(APIView):
    def get(self, request, *args, **kwargs):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FoodDetail(APIView):
    
    
        
    
    def get(self, request, pk=None, *args, **kwargs):
        food = get_object_or_404(Food, id=pk)
        serializer = FoodSerializer(food)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk=None, *args, **kwargs):
        food = get_object_or_404(Food, id=pk)
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        food = get_object_or_404(Food, id=pk)
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)