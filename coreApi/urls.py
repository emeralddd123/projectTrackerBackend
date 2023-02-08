from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from .views import TaskListApiView, TaskDetailApiView

urlpatterns = [
    path('notes', TaskListApiView.as_view(), name='tasklist'),
    path('notes/<slug>', TaskDetailApiView.as_view(), name='task-view'),
    
    path('docs', include_docs_urls(title='Project Tracker API')),
    path('schema', get_schema_view(
        title='Project Tracker API',
        description='API for Project Tracker',
        version='1.1.0',
        
        ),name='open-api schema' ),
]
