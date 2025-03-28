from typing import Any

from rest_framework import serializers,exceptions
from rest_framework_simplejwt.tokens import Token

from .models import User,Department, UserStatusChoices,Permission
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar', 'bio', 
                 'birth_date', 'department']
        read_only_fields = ['email']  # 邮箱不允许通过此接口修改
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password','last_login')

    def get_roles(self, obj):
        return list(obj.role.all().values_list('name', flat=True))

    def get_permissions(self, obj):
        roles = obj.role.all()
        return list(Permission.objects.filter(
            rolepermission__role__in=roles
        ).values_list("codename", flat=True).distinct())

class CustomLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)
        user_serializer = UserSerializer(user)
        token['user_info'] = user_serializer.data
        # 添加角色和权限信息到token中
        token['roles'] = user_serializer.get_roles(user)
        token['permissions'] = user_serializer.get_permissions(user)
        return token

    def validate(self, attrs: dict[str, Any]) -> dict[str, str]:
        data = super().validate(attrs)
        user = self.user
        user_serializer = UserSerializer(user)
        new_data = user_serializer.data
        data['user'] = new_data
        return data


class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6,max_length=20)
    pwd1 = serializers.CharField(min_length=6,max_length=20)
    pwd2 = serializers.CharField(min_length=6,max_length=20)

    def validate(self, attrs):
        oldpwd = attrs.get('oldpwd')
        pwd1 = attrs.get('pwd1')
        pwd2 = attrs.get('pwd2')

        user = self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError("旧密码错误")
        if pwd1 != pwd2:
            raise exceptions.ValidationError("两个新密码不一致")
        return attrs

