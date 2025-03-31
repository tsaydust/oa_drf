from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Salary
from .serializers import SalarySerializer
from apps.oaauth.permissions import RBACPermission


class SalaryViewSet(viewsets.ModelViewSet):
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [RBACPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        # 处理查询参数
        params = self.request.query_params

        # 按时间范围过滤
        start_date = params.get('start_date')
        end_date = params.get('end_date')
        if start_date:
            queryset = queryset.filter(effective_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(effective_date__lte=end_date)

        # 按薪资范围过滤
        min_amount = params.get('min_amount')
        max_amount = params.get('max_amount')
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)

        # 按部门过滤
        department_id = params.get('department_id')
        if department_id:
            queryset = queryset.filter(employee__department_id=department_id)

        # 按角色权限过滤
        if user.has_role('admin'):
            return queryset
        elif user.has_role('manager'):
            return queryset.filter(employee__department_id=user.department_id)
        else:
            return queryset.filter(employee=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
