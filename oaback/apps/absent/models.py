from django.db import models
from django.contrib.auth import get_user_model
from apps.oaauth.models import Department

User = get_user_model()


class AbsentStatusChoices(models.IntegerChoices):
    # 审批中
    AUDITING = 1
    # 审核通过
    PASS = 2
    # 审核拒绝
    REJECT = 3


class AbsentType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "absent_type"


class Absent(models.Model):
    # 1. 标题
    title = models.CharField(max_length=200)
    # 2. 请假详细内容
    request_content = models.TextField()
    # 3. 请假类型（事假、婚假）
    absent_type = models.ForeignKey(AbsentType, on_delete=models.CASCADE, related_name='absents',
                                    related_query_name='absents')
    # 如果在一个模型中，有多个字段对同一个模型引用了外键，那么必须指定related_name为不同的值
    # 4. 发起人
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_absents',
                                  related_query_name='my_absents')
    # 5. 考勤所属部门
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='sub_absents',
                                   related_query_name='sub_absents', null=True)
    # 6. 状态
    status = models.IntegerField(
        choices=AbsentStatusChoices, default=AbsentStatusChoices.AUDITING)
    # 7. 请假开始日期
    start_date = models.DateField()
    # 8. 请假结束日期
    end_date = models.DateField()
    # 9. 请假发起时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 10. 审批回复内容
    response_content = models.TextField(blank=True)

    @property
    def department_manager(self):
        """获取请假申请所属部门的领导"""
        return User.objects.filter(
            department=self.department,
            role__name='manager'
        ).first()

    class Meta:
        db_table = "absent"
        ordering = ('-create_time',)
