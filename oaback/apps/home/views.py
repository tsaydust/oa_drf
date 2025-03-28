from rest_framework.views import APIView
from apps.inform.models import Inform, InformRead
from apps.inform.serializers import InformSerializer
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework. response import Response
from apps.absent.models import Absent
from apps.absent.serializers import AbsentSerializer
from apps.oaauth.models import Department
from django.db.models import Count
from utils.skip_auth import allow_any


class LatestInformView(APIView):
    def get(self, request):
        user = request.user
        informs = Inform.objects.prefetch_related(Prefetch("reads", queryset=InformRead.objects.filter(user_id=user.id)), 'departments').filter(Q(public=True) | Q(departments=user.department))[:10]
        serializer = InformSerializer(informs, many=True)
        return Response(serializer.data)


class LatestAbsentView(APIView):
    def get(self, request):
        # 董事会的人，可以看到所有人的考勤信息，非董事会的人，只能看到自己部门的考勤信息
        user = request.user
        queryset = Absent.objects
        if not user.has_role('admin'):
            queryset = queryset.filter(requester__department_id=user.department_id)
        queryset = queryset.all()[:6]
        serializer = AbsentSerializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentStaffCountView(APIView):
    def get(self, request):
        rows = Department.objects.annotate(staff_count=Count("employees")).values("name", "staff_count")
        return Response(rows)

@allow_any
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"code": 200})