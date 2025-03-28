from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ResetPwdSerializer, CustomLoginSerializer, UserProfileSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {'detail': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ResetPwdView(APIView):
    def post(self, request):
        serializer = ResetPwdSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data.get('pwd1')
            request.user.set_password(pwd1)
            request.user.save()
            return Response()
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """获取个人信息"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """更新个人信息"""
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
