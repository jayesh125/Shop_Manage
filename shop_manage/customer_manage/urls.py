from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('', include(router.urls)),
]