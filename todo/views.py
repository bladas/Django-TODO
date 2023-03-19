from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from todo.models import Task, TaskStatus, Comments
from todo.permissions import TaskAuthorPermission, CommentAuthorPermission
from todo.serializers import TaskModelSerializer, TaskStatusModelSerializer, CommentsModelSerializer


class TasksModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & TaskAuthorPermission]
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status__name']


class TaskStatusModelViewSet(ModelViewSet):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusModelSerializer


class CommentsModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated & CommentAuthorPermission]
    queryset = Comments.objects.all()
    serializer_class = CommentsModelSerializer

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        return self.queryset.filter(task__id=task_id)
