from rest_framework import viewsets, mixins, status
from .models import AbsentType, Absent
from .serializers import AbsentSerializer, AbsentTypeSerializer
from rest_framework.generics import ListAPIView
from apps.oaauth.permissions import RBACPermission
from rest_framework.response import Response


class AbsentViewSet(viewsets.ModelViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer
    permission_classes = [RBACPermission]
    required_role_put = "manager"

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        """根据用户角色动态过滤查询集"""
        queryset = super().get_queryset()
        user = self.request.user
        if user.has_role("admin"):
            return queryset
        if user.has_role("manager"):
            return queryset.filter(department=user.department_id)
        return queryset.filter(requester_id=user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        goal = request.query_params.get('goal')
        
        result = queryset
        if goal == 'mine':
            result = queryset.filter(requester=request.user)
        
        # 使用 DRF 的分页功能
        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class AbsentTypeView(ListAPIView):
    serializer_class = AbsentTypeSerializer
    queryset = AbsentType.objects.all()
    permission_classes = [RBACPermission]



