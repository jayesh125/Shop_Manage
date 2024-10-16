from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from shop_manage.renders import UserRenderer

# Create your views here.

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'address', 'phone']
    search_fields = ['name', 'phone']

    def check_permissions(self, request):
        self.permission_classes = [IsAuthenticated]
        super().check_permissions(request)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
