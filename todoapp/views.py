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
    permission_classes = [IsAuthenticated]
    
    def get(self,request,pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
            serializer = TodoSerializer(todo,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        try:
            todo = Todo.objects.get(pk=pk, user=request.user)
            todo.delete()
            return Response({'message': 'Todo deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Todo.DoesNotExist:
            return Response({'error': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request):
        print(request.data)
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
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': f'Hello, {request.user.username}! You are authenticated.'})