"""
Views for the branch APIs
"""
from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Branch,
    Skill,
    Service,
    Payment,
    Discount,
    Promo,
    Client,
    Appointment,
    Technician
)
from salon import serializers


class BranchViewSet(viewsets.ModelViewSet):
    """View for manage branch APIs."""
    serializer_class = serializers.BranchSerializer
    queryset = Branch.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]


class SkillViewSet(viewsets.ModelViewSet):
    """View for manage skill APIs."""
    serializer_class = serializers.SkillSerializer
    queryset = Skill.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ServiceViewSet(viewsets.ModelViewSet):
    """View for manage service APIs"""
    serializer_class = serializers.ServiceSerializer
    queryset = Service.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PaymentViewSet(viewsets.ModelViewSet):
    """View for manage payment APIs"""
    serializer_class = serializers.PaymentSerializer
    queryset = Payment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class DiscountViewSet(viewsets.ModelViewSet):
    """View for manage discount APIs"""
    serializer_class = serializers.DiscountSerializer
    queryset = Discount.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PromoViewSet(viewsets.ModelViewSet):
    """View for manage promo APIs"""
    serializer_class = serializers.PromoSerializer
    queryset = Promo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ClientViewSet(viewsets.ModelViewSet):
    """View for manage client APIs"""
    serializer_class = serializers.ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TechnicianViewSet(viewsets.ModelViewSet):
    """View for manage technician APIs"""
    serializer_class = serializers.TechnicianSerializer
    queryset = Technician.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(viewsets.ModelViewSet):
    """View for manage appointment APIs"""
    serializer_class = serializers.AppointmentSerializer
    queryset = Appointment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
