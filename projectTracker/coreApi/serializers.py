from rest_framework.serializers import ModelSerializer
from .models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        db_table =''
        managed = True
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        
        fields = ['user', 'title', 'slug', 'description', 'priority', 'status', 'date', 'remind']
        

