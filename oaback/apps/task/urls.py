from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


router = DefaultRouter(trailing_slash=False)
router.register('task', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
