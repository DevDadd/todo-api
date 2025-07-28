from django.urls import path,include
from . import views
urlpatterns = [
    path('list/', views.TodoList.as_view(), name='todo_list'),
    path('<int:pk>/', views.TodoDetail.as_view(), name='todo_detail'),
]