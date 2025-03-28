from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

def allow_any(view_func):
    """
    装饰视图，允许匿名访问（跳过 JWT 认证）
    """
    return permission_classes([AllowAny])(view_func)
