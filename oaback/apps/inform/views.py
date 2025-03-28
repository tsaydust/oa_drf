from rest_framework import viewsets
from .models import Inform, InformRead
from .serializers import InformSerializer
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Prefetch
from apps.oaauth.permissions import RBACPermission

class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer
    permission_classes = [RBACPermission]

    required_role_post = "manager"
    required_role_delete= "manager"
    required_role_put = "manager"

    def get_queryset(self):
        queryset = self.queryset.select_related('author').prefetch_related(Prefetch("reads", queryset=InformRead.objects.filter(user_id=self.request.user.id)), 'departments').filter(Q(public=True) | Q(departments=self.request.user.department) | Q(author=self.request.user)).distinct()
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.id == request.user.id:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['read_count'] = InformRead.objects.filter(inform_id=instance.id).count()
        return Response(data=data)


# class ReadInformView(APIView):
#     def post(self, request):
#         # 通知的id
#         serializer = ReadInformSerializer(data=request.data)
#         if serializer.is_valid():
#             inform_pk = serializer.validated_data.get('inform_pk')
#             if InformRead.objects.filter(inform_id=inform_pk, user_id=request.user.id).exists():
#                 return Response()
#             else:
#                 try:
#                     InformRead.objects.create(inform_id=inform_pk, user_id=request.user.id)
#                 except Exception as e:
#                     print(e)
#                     return Response(status=status.HTTP_400_BAD_REQUEST)
#                 return Response()
#         else:
#             return Response(data={'detail': list(serializer.errors.values())[0][0]}, status=status.HTTP_400_BAD_REQUEST)