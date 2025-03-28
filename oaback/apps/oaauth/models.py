from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserStatusChoices(models.IntegerChoices):
    # 已经激活的
    ACTIVED = 1
    # 没有激活
    UNACTIVE = 2
    # 被锁定
    LOCKED = 3


class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 部门名称
    leader = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='leading_department')  # 部门负责人

    class Meta:
        db_table = "department"


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})
    
    def create_user(self, email, username, password, department_id=None, role=None, **extra_fields):
        if not email:
            raise ValueError('邮箱是必填项')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        
        if department_id:
            user.department_id = department_id
            
        user.save(using=self._db)
        
        # 分配角色
        employee_role = Role.objects.get(name='employee')
        user.role.add(employee_role)
        
        # 如果是leader，添加manager角色
        if role == 'leader':
            manager_role = Role.objects.get(name='manager')
            user.role.add(manager_role)
            
        # 如果是董事会部门(id=1)，添加admin角色
        if department_id == 1:
            admin_role = Role.objects.get(name='admin')
            user.role.add(admin_role)
            
        return user


class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "role"


class User(AbstractBaseUser):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)  # 邮箱（唯一）
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)  # 手机号（唯一，可选）
    avatar = models.URLField(max_length=500, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # 个人简介
    birth_date = models.DateField(blank=True, null=True)  # 生日

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='employees')  # 所属部门
    status = models.IntegerField(choices=UserStatusChoices, default=UserStatusChoices.UNACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)  # 记录用户创建时间
    role = models.ManyToManyField(Role, related_name="users", blank=True)
    # 指定用于登录的字段
    USERNAME_FIELD = 'email'
    # 指定创建用户时必需的字段
    REQUIRED_FIELDS = []
    # 使用自定义用户管理器
    objects = CustomUserManager()

    def has_perm(self,perm):
        roles = self.role.all()
        permissions = Permission.objects.filter(rolepermission__role__in=roles).values_list("codename", flat=True)
        return perm in permissions

    def has_role(self,role):
        roles = self.role.all().values_list("name",flat=True)
        return role in roles

    def get_admin_users(self):
        admin_role = Role.objects.get(name="admin")
        return User.objects.filter(role=admin_role).first()


    class Meta:
        db_table = "user"
        ordering = ['-created_at']  # 默认按创建时间倒序排列


class Permission(models.Model):
    name = models.CharField(max_length=20, unique=True)
    codename = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "permission"


# class UserRole(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roles")
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "user_role"
#         unique_together = ('user', 'role')


class RolePermission(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "role_permission"
        unique_together = ('role', 'permission')
