from django.shortcuts import render
from .models import Todo
from .serializer import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TodoList(APIView):
    def get(self,request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class TodoDetail(APIView):
    def get(self,request,pk):
        todo = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    def put(self,request,pk):
        todo = Todo.objects.get(pk=pk)
        serializer = TodoSerializer(todo,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        todo = Todo.objects.get(pk=pk)
        todo.delete()
# Create your views here.
