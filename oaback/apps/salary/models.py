from django.db import models
from django.conf import settings


class Salary(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='salaries')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='薪资金额')
    effective_date = models.DateField(verbose_name='生效日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_salaries',
        verbose_name='创建者'
    )

    class Meta:
        db_table = 'salary'
        ordering = ['-effective_date']


