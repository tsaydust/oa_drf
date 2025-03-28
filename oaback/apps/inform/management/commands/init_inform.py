from django.core.management.base import BaseCommand
from apps.inform.models import Inform
from apps.oaauth.models import User, Department
from django.db import transaction


class Command(BaseCommand):
    help = '初始化通知数据'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # 获取董事会部门和其他部门
                board = Department.objects.get(name='董事会')
                hr = Department.objects.get(name='人力资源部')
                tech = Department.objects.get(name='技术部')
                finance = Department.objects.get(name='财务部')

                # 获取CEO用户（用于创建全公司通知）
                ceo = User.objects.get(email='ceo@gmail.com')
                
                # 创建一个全公司可见的通知
                company_inform = Inform.objects.create(
                    title='公司年度计划通知',
                    content='各部门同事：\n\n2024年度工作计划已经制定完成，请各部门负责人及时查看并执行。\n\n祝工作顺利！',
                    author=ceo,
                    public=True
                )

                # 创建一个只有技术部可见的通知
                tech_inform = Inform.objects.create(
                    title='技术部周会通知',
                    content='技术部全体同事：\n\n本周五下午3点召开技术部周会，请准时参加。\n\n会议地点：会议室A',
                    author=User.objects.get(email='tech_leader@gmail.com'),
                    public=False
                )
                tech_inform.departments.add(tech)

                # 创建一个人力资源部可见的通知
                hr_inform = Inform.objects.create(
                    title='入职培训通知',
                    content='各位新入职员工：\n\n欢迎加入我们的团队！入职培训将于下周一上午9点开始。\n\n请准时参加！',
                    author=User.objects.get(email='hr_leader@gmail.com'),
                    public=False
                )
                hr_inform.departments.add(hr)

                # 创建一个财务部可见的通知
                finance_inform = Inform.objects.create(
                    title='报销制度更新通知',
                    content='财务部门全体同事：\n\n公司报销制度已更新，请查看附件了解详情。\n\n如有疑问请及时反馈。',
                    author=User.objects.get(email='finance_leader@gmail.com'),
                    public=False
                )
                finance_inform.departments.add(finance)

                # 创建一个多部门可见的通知
                multi_dept_inform = Inform.objects.create(
                    title='项目协作通知',
                    content='技术部与财务部同事：\n\n关于新系统的开发预算会议将于下周二下午2点举行。\n\n请相关同事准时参加。',
                    author=ceo,
                    public=False
                )
                multi_dept_inform.departments.add(tech, finance)

                self.stdout.write(self.style.SUCCESS('成功初始化通知数据'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'初始化通知数据失败: {str(e)}'))