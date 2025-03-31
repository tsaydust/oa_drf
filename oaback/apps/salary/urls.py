from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'salary'

router = DefaultRouter(trailing_slash=False)
router.register('records', views.SalaryViewSet, basename='salary')

urlpatterns = [
    path('', include(router.urls)),
]
