from django.db import models
from apps.oaauth.models import User, Department


class Inform(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 如果前端上传的department_ids中包含了0，比如[0]，那么就认为这个通知是所有部门可见
    public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='informs', related_query_name='informs')
    # departments：序列化的时候用，前端上传部门id，我们通过department_ids来获取
    departments = models.ManyToManyField(Department, related_name='informs', related_query_name='informs')

    class Meta:
        db_table= "inform"
        ordering = ('-create_time', )


class InformRead(models.Model):
    inform = models.ForeignKey(Inform, on_delete=models.CASCADE, related_name='reads', related_query_name='reads')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reads', related_query_name='reads')
    read_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table="inform_read"
        # inform和user组合的数据，必须是唯一的
        unique_together = ('inform', 'user')
