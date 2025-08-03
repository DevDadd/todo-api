from django.shortcuts import render
from .models import Todo
from .serializer import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

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

class RegisterView(APIView):
        permission_classes = [AllowAny]
        def post(self,request):
            username = request.data.get('username')
            password = request.data.get('password')

            if User.objects.filter(username=username).exists():
                return Response({'error':'Username already exists'},status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.create_user(username=username,password=password)
            return Response({'message':'User created successfully'},status=status.HTTP_201_CREATED)

class TodoList(APIView):
     permission_classes = [IsAuthenticated]
     def get(self,request):
          todos = Todo.objects.filter(user=request.user)
          data = [{'id':todo.id,'title':todo.title,'description':todo.description,'completed':todo.completed} for todo in todos]
          return Response(data)