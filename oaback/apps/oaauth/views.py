from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.shortcuts import redirect
import requests
from .serializers import ResetPwdSerializer, CustomLoginSerializer, UserProfileSerializer, UserSerializer
from .models import User


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
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GitHubLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """获取GitHub授权URL"""
        github_auth_url = f'https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.GITHUB_CALLBACK_URL}&scope=user:email'
        return Response({'auth_url': github_auth_url})


class GitHubCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """处理GitHub回调"""
        code = request.GET.get('code')
        if not code:
            return Response({'error': '未获取到授权码'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取访问令牌
        token_url = 'https://github.com/login/oauth/access_token'
        response = requests.post(token_url, data={
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'code': code
        }, headers={'Accept': 'application/json'})
        token_data = response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return Response({'error': '获取访问令牌失败'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取用户信息
        user_url = 'https://api.github.com/user'
        user_response = requests.get(user_url, headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        })
        github_user = user_response.json()

        # 获取用户邮箱
        email_url = 'https://api.github.com/user/emails'
        email_response = requests.get(email_url, headers={
            'Authorization': f'token {access_token}',
            'Accept': 'application/json'
        })
        emails = email_response.json()
        primary_email = next((email['email']
                             for email in emails if email['primary']), None)

        # 创建或更新用户
        # 创建或更新用户，使用更复杂的默认密码
        default_password = "123456"
        user, created = User.objects.get_or_create(
            email=primary_email,
            defaults={
                'username': github_user['login'],
                'avatar': github_user.get('avatar_url'),
                'bio': github_user.get('bio', ''),
                'status': "1",
                "department_id":"1",
            }
        )
        if created:
            user.set_password(default_password)
            user.save()

        # 生成JWT令牌
        serializer = CustomLoginSerializer()
        token = serializer.get_token(user)
        refresh = serializer.get_token(user)
        return Response({
            'access': str(token.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        })
