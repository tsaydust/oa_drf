# Generated by Django 5.0.3 on 2025-03-22 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oaauth', '0004_remove_user_is_board_member_remove_user_is_manager_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='updated_at',
        ),
    ]
