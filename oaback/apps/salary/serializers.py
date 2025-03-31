from rest_framework import serializers
from .models import Salary
from django.contrib.auth import get_user_model

OAUser = get_user_model()


class SalarySerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source='employee.username', read_only=True)
    created_by_name = serializers.CharField(
        source='created_by.username', read_only=True)

    class Meta:
        model = Salary
        fields = ['id', 'employee', 'employee_name', 'amount', 'effective_date',
                  'created_at', 'updated_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.has_role('admin') and not request.user.has_role('manager'):
            raise serializers.ValidationError('您没有权限操作薪资记录！')
        if request.user.has_role('admin'):
            return attrs
        # 如果是manager，只能操作本部门员工的薪资
        if request.user.has_role('manager'):
            employee = attrs.get('employee')
            if employee.department_id != request.user.department_id:
                raise serializers.ValidationError('您只能操作本部门员工的薪资记录！')
        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
