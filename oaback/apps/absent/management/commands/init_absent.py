from django.core.management.base import BaseCommand
from apps.absent.models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.models import User, Department
from django.db import transaction
from datetime import date, timedelta


class Command(BaseCommand):
    help = '初始化考勤数据'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # 获取部门和用户
                tech_dept = Department.objects.get(name='技术部')
                hr_dept = Department.objects.get(name='人力资源部')
                
                tech_employee = User.objects.get(email='tech1@gmail.com')
                hr_employee = User.objects.get(email='hr1@gmail.com')

                # 获取请假类型
                sick_leave = AbsentType.objects.get(name='病假')
                personal_leave = AbsentType.objects.get(name='事假')
                marriage_leave = AbsentType.objects.get(name='婚假')

                # 创建一些审批中的请假
                Absent.objects.create(
                    title='感冒请假',
                    request_content='最近感冒发烧，需要休息两天',
                    absent_type=sick_leave,
                    requester=tech_employee,
                    department=tech_dept,
                    status=AbsentStatusChoices.AUDITING,
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=2)
                )

                # 创建一个已通过的请假
                Absent.objects.create(
                    title='婚假申请',
                    request_content='计划下月结婚，申请婚假',
                    absent_type=marriage_leave,
                    requester=hr_employee,
                    department=hr_dept,
                    status=AbsentStatusChoices.PASS,
                    start_date=date.today() + timedelta(days=30),
                    end_date=date.today() + timedelta(days=37),
                    response_content='祝贺！批准请假。'
                )

                # 创建一个被拒绝的请假
                Absent.objects.create(
                    title='事假申请',
                    request_content='需要处理个人事务，请假一天',
                    absent_type=personal_leave,
                    requester=tech_employee,
                    department=tech_dept,
                    status=AbsentStatusChoices.REJECT,
                    start_date=date.today() - timedelta(days=5),
                    end_date=date.today() - timedelta(days=5),
                    response_content='本周工作任务较重，暂不能批准。'
                )

                self.stdout.write(self.style.SUCCESS('成功初始化考勤数据'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'初始化考勤数据失败: {str(e)}'))