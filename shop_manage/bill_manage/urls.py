from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet

router = DefaultRouter()
router.register(r'bills', BillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
