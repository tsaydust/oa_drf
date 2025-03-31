from rest_framework import serializers
from .models import Task
from apps.oaauth.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)
    assignee_info = UserSerializer(source='assignee', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'content', 'creator', 'assignee', 'status','department',
                  'created_at', 'updated_at', 'creator_info', 'assignee_info']
        read_only_fields = ['creator', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        assignee = attrs.get('assignee')

        if user.has_role('manager') and assignee.department_id != user.department_id and not user.has_role('admin'):
            raise serializers.ValidationError('只能给自己部门的成员发布任务')

        return attrs
