"""
URL mappings for the branch app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from salon import views


router = DefaultRouter()
router.register('branches', views.BranchViewSet)
router.register('skills', views.SkillViewSet)
router.register('services', views.ServiceViewSet)
router.register('payments', views.PaymentViewSet)
router.register('discounts', views.DiscountViewSet)
router.register('promos', views.PromoViewSet)
router.register('clients', views.ClientViewSet)
router.register('appointments', views.AppointmentViewSet)
router.register('technicians', views.TechnicianViewSet)

app_name = 'salon'

urlpatterns = [
    path('', include(router.urls)),
]
