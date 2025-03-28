from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'staff'

router = DefaultRouter(trailing_slash=False)
router.register('staff', views.StaffViewSet, basename='staff')

urlpatterns = [
    path('departments', views.DepartmentListView.as_view(), name='departments'),
    path('active', views.ActiveStaffView.as_view(), name='active_staff'),
    path('download', views.StaffDownloadView.as_view(), name='download_staff'),
    path('upload', views.StaffUploadView.as_view(), name='upload_staff'),
] + router.urls