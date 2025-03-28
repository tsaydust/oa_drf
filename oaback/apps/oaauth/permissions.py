from rest_framework.permissions import BasePermission


class RBACPermission(BasePermission):
    def has_permission(self, request, view):
        # 尝试获取针对特定方法的权限设置
        method = request.method.lower()

        # 查找方法特定的权限设置
        method_role = getattr(view, f'required_role_{method}', None)
        method_permission = getattr(view, f'required_permission_{method}', None)

        # 如果没有方法特定的设置，则回退到通用设置
        required_role = method_role or getattr(view, 'required_role', None)
        required_permission = method_permission or getattr(view, 'required_permission', None)

        # 如果没有设置权限要求，默认允许访问
        if not required_role and not required_permission:
            return True

        # 检查用户是否具有指定的角色
        if required_role and request.user.has_role(required_role):
            return True

        # 检查用户是否具有指定的权限
        if required_permission and request.user.has_perm(required_permission):
            return True
