from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, token_obtain_pair, token_verify, token_refresh

app_name = 'oaauth'

urlpatterns = [
    path('token/refresh', token_refresh, name="refresh"),
    path('login', views.LoginView.as_view(), name='login'),
    path('resetpwd', views.ResetPwdView.as_view(), name='resetpwd'),
    path('profile', views.UserProfileView.as_view(), name='user-profile'),
    path('github/login', views.GitHubLoginView.as_view(), name='github-login'),
    path('github/callback', views.GitHubCallbackView.as_view(),
         name='github-callback'),
]
