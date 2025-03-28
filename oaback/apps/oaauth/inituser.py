from apps.oaauth.models import Role, Permission, Department, User, RolePermission
from django.db import transaction


def init_data():
    try:
        with transaction.atomic():
            # 1. 创建角色
            admin_role = Role.objects.create(
                name='admin',
                description='系统管理员'
            )
            manager_role = Role.objects.create(
                name='manager',
                description='部门管理者'
            )
            employee_role = Role.objects.create(
                name='employee',
                description='普通员工'
            )

            # 2. 创建权限
            upload_perm = Permission.objects.create(
                name='上传文件',
                codename='upload'
            )
            download_perm = Permission.objects.create(
                name='下载文件',
                codename='download'
            )

            # 3. 角色权限关联
            # admin拥有所有权限
            RolePermission.objects.create(role=admin_role, permission=upload_perm)
            RolePermission.objects.create(role=admin_role, permission=download_perm)
            # manager只有下载权限
            RolePermission.objects.create(role=manager_role, permission=download_perm)

            # 4. 创建部门
            board = Department.objects.create(name='董事会')
            hr = Department.objects.create(name='人力资源部')
            tech = Department.objects.create(name='技术部')
            finance = Department.objects.create(name='财务部')
            
            # 5. 创建用户
            # 董事会成员（具有所有角色）
            ceo = User.objects.create_user(
                email='ceo@gmail.com',
                username='张总',
                password='123456',
                department_id=board.id
            )
            ceo.role.add(admin_role, manager_role, employee_role)
            board.leader = ceo
            board.save()

            # 各部门负责人（具有manager和employee角色）
            hr_leader = User.objects.create_user(
                email='hr_leader@gmail.com',
                username='王经理',
                password='123456',
                department_id=hr.id,
                role='leader'
            )
            hr.leader = hr_leader
            hr.save()

            tech_leader = User.objects.create_user(
                email='tech_leader@gmail.com',
                username='李经理',
                password='123456',
                department_id=tech.id,
                role='leader'
            )
            tech.leader = tech_leader
            tech.save()

            finance_leader = User.objects.create_user(
                email='finance_leader@gmail.com',
                username='赵经理',
                password='123456',
                department_id=finance.id,
                role='leader'
            )
            finance.leader = finance_leader
            finance.save()

            # 普通员工（只有employee角色）
            User.objects.create_user(
                email='hr1@gmail.com',
                username='小王',
                password='123456',
                department_id=hr.id
            )

            User.objects.create_user(
                email='tech1@gmail.com',
                username='小李',
                password='123456',
                department_id=tech.id
            )

            User.objects.create_user(
                email='finance1@gmail.com',
                username='小赵',
                password='123456',
                department_id=finance.id
            )

            print('成功初始化基础数据')

    except Exception as e:
        print(f'初始化数据失败: {str(e)}')