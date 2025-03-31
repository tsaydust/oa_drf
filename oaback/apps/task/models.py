from django.db import models
from apps.oaauth.models import User, Department


class Task(models.Model):
    TASK_STATUS = [
        ('pending', '待处理'),
        ('completed', '已完成'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField(verbose_name='任务内容')
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='assigned_tasks')
    status = models.CharField(
        max_length=20, choices=TASK_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='department_tasks', null=True)

    class Meta:
        db_table = 'task'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
