from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from apps.oaauth.permissions import RBACPermission


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [RBACPermission]
    required_role = 'employee'

    def get_queryset(self):
        user = self.request.user
        if user.has_role('admin'):
            return Task.objects.all()
        if user.has_role('manager'):
            return Task.objects.filter(assignee__department=user.department_id)
        return Task.objects.filter(assignee=user)

    def perform_create(self, serializer):
        if not (self.request.user.has_role('admin') or self.request.user.has_role('manager')):
            return Response({'error': '只有管理员和经理可以创建任务'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        task = self.get_object()
        if task.assignee != request.user:
            return Response({'error': '只有任务执行者可以完成任务'}, status=status.HTTP_403_FORBIDDEN)
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
