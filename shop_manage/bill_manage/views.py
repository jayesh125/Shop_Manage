from rest_framework import viewsets
from .models import Bill
from .serializers import BillSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from shop_manage.renders import UserRenderer

class BillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing bills.
    """
    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]

    queryset = Bill.objects.all()
    serializer_class = BillSerializer

    filter_backends = [SearchFilter]
    search_fields = ['name', 'bill_number']
