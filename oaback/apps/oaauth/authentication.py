from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    InvalidSignatureError,
    DecodeError
)

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            user_auth_tuple = super().authenticate(request)
            if user_auth_tuple is None:
                return None
            user, token = user_auth_tuple
            request.user = user
            request.auth = token
            return user, token

        except ExpiredSignatureError:
            raise AuthenticationFailed("Token已过期，请重新登录！")
            
        except InvalidSignatureError:
            raise AuthenticationFailed("无效的Token签名！")
            
        except DecodeError:
            raise AuthenticationFailed("Token解析失败，请检查Token格式！")
            
        except InvalidTokenError:
            raise AuthenticationFailed("无效的Token！")

        except Exception as e:
            raise AuthenticationFailed(f"认证失败: {str(e)}")
