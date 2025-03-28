from rest_framework import serializers, exceptions
from .models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.serializers import UserSerializer


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only=True)
    department_manager = UserSerializer(read_only=True)  # 添加部门领导字段

    class Meta:
        model = Absent
        fields = '__all__'

    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError('考勤类型不存在')
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        absent = Absent.objects.create(**validated_data, requester=user, department=user.department)
        return absent

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail="不能修改已经确定的请假数据")
        instance.status = validated_data['status']
        instance.response_content = validated_data['response_content']
        instance.save()
        return instance
