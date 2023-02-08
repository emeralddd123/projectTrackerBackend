from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TaskSerializer
from .models import Task
# Create your views here.
class TaskListApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    def get(self, request, *args, **kwargs):
        '''
        List all the note items for given requested user
        '''
        notes = Task.objects.filter(user = request.user.id)
        serializer = TaskSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create 
    def post(self, request, *args, **kwargs):
        '''
        Create a Note with given note data
        '''
        data = {
            'user': request.user.id,
            'title': request.data.get('title'), 
            'description': request.data.get('description'),
            'priority': request.data.get('priority'),
            'status': request.data.get('status'),
            'date': request.data.get('date'),
            'remind': request.data.get('remind')
            }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailApiView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    
    """
    Retrieve, update or delete a note instance.
    """
    def get_object(self, slug):
        task = get_object_or_404(Task, slug=slug)
        return task

    def get(self, request, slug):
        task = self.get_object(slug)
        try:
            task = get_object_or_404(Task, slug=slug)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except task == 404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, slug):
        task = self.get_object(slug)
        serializer = TaskSerializer(task, data=request.data, partial=True )
        serializer.initial_data['slug']=slug        # to keep the initial slug unchanged
        serializer.initial_data['user']=request.user.id #prevent reassigning task to another user
        if serializer.is_valid():
            #serializer.validated_data['slug']=note_slug
            #Note.delete(slug=note_slug)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        task = self.get_object(slug)
        if task:
            task.delete()
            return Response("OK")
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    