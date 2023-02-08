from django.urls import path, include
from .views import TaskListApiView, TaskDetailApiView

urlpatterns = [
    path('', TaskListApiView.as_view(), name='tasklist'),
    path('notes/<slug>', TaskDetailApiView.as_view(), name='task-view')
    
]
