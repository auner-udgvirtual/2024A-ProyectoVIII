"""
Serializers for branch APIs
"""
from rest_framework import serializers

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

from user.serializers import UserSerializer
from core.models import User


class BranchSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Branch
        fields = ['id', 'name', 'address', 'start_time', 'end_time']
        read_only_fields = ['id']


class SkillSerializer(serializers.ModelSerializer):
    """Serializer for skills."""

    class Meta:
        model = Skill
        fields = ['id', 'name']
        read_only_fields = ['id']


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Services."""

    class Meta:
        model = Service
        fields = ['id', 'name', 'price']
        read_only_fields = ['id']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payments"""

    class Meta:
        model = Payment
        fields = ['id', 'format_code', 'description']
        read_only_fields = ['id']


class DiscountSerializer(serializers.ModelSerializer):
    """Serializer for Discount"""

    class Meta:
        model = Discount
        fields = ['id', 'description', 'value']
        read_only_fields = ['id']


class PromoSerializer(serializers.ModelSerializer):
    """Serializer for Promos"""

    class Meta:
        model = Promo
        fields = ['id', 'weekday', 'name']
        read_only_fields = ['id']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Clients"""

    class Meta:
        model = Client
        fields = ['id', 'name', 'last_name',
                  'phone', 'email', 'birthday', 'comments']
        read_only_fields = ['id']


class TechnicianSerializer(serializers.ModelSerializer):
    """Serializer for Technician"""
    user = UserSerializer()
    skills = SkillSerializer(many=True, required=False)
    branches = BranchSerializer(many=True, required=False)

    class Meta:
        model = Technician
        fields = ['id', 'user', 'skills', 'branches']
        read_only_fields = ['id']

    def get_or_create_user(self, validated_data):
        """Handle getting or creating user as needed."""
        user_data = validated_data.pop('user')
        user = User.objects.get_or_create(**user_data)
        return user

    def get_or_create_skills(self, validated_data):
        """Handle getting or creating skills as needed."""
        skills_data = validated_data.pop('skills')
        skills = []
        for skill_data in skills_data:
            skill = Skill.objects.get_or_create(**skill_data)
            skills.append(skill)
        return skills

    def get_or_create_branches(self, validated_data):
        """Handle getting or creating branches as needed."""
        branches_data = validated_data.pop('branches')
        branches = []
        for branch_data in branches_data:
            branch = Branch.objects.get_or_create(**branch_data)
            branches.append(branch)
        return branches

    def create(self, validated_data):
        """Create and return a new technician."""
        user = validated_data.pop('user')
        skills = validated_data.pop('skills', [])
        branches = validated_data.pop('branches', [])
        technician = Technician.objects.create(**validated_data)

        self.get_or_create_user(user, technician)
        self.get_or_create_skills(skills, technician)
        self.get_or_create_branches(branches, technician)

        return technician

    def update(self, instance, validated_data):
        """Update technician."""
        user = validated_data.pop('user')
        skills = validated_data.pop('skills', None)
        branches = validated_data.pop('branches', None)
        if user is not None:
            instance.user.clear()
            self.get_or_create_user(user, instance)

        if skills is not None:
            instance.skills.clear()
            self.get_or_create_skills(skills, instance)

        if branches is not None:
            instance.branches.clear()
            self.get_or_create_branches(branches, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for Appointments"""
    branch = BranchSerializer()
    client = ClientSerializer()
    technician = TechnicianSerializer()
    service = ServiceSerializer()
    payment = PaymentSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = Appointment
        fields = ['id', 'date', 'time', 'branch', 'client', 'technician',
                  'service', 'warranty', 'payment', 'commission', 'tip',
                  'courtesy', 'discount', 'discount_price', 'final_income', ]
        read_only_fields = ['id']

    def get_or_create_branch(self, branch, appointment):
        """Handle getting or creating branch as needed."""
        branch = Branch.objects.get_or_create(**branch)
        appointment.branch.add(branch)

    def get_or_create_client(self, client, appointment):
        """Handle getting or creating client as needed."""
        client = Client.objects.get_or_create(**client)
        appointment.client.add(client)

    def get_or_create_technician(self, technician, appointment):
        """Handle getting or creating technician as needed."""
        technician = Technician.objects.get_or_create(**technician)
        appointment.technician.add(technician)

    def get_or_create_service(self, service, appointment):
        """Handle getting or creating service as needed."""
        service = Service.objects.get_or_create(**service)
        appointment.service.add(service)

    def get_or_create_payment(self, payment, appointment):
        """Handle getting or creating payment as needed."""
        payment = Payment.objects.get_or_create(**payment)
        appointment.payment.add(payment)

    def get_or_create_discount(self, discount, appointment):
        """Handle getting or creating discount as needed."""
        discount = Discount.objects.get_or_create(**discount)
        appointment.discount.add(discount)

    def create(self, validated_data):
        """Create and return a new appointment."""
        branch = validated_data.pop('branch')
        client = validated_data.pop('client')
        technician = validated_data.pop('technician')
        service = validated_data.pop('service')
        payment = validated_data.pop('payment')
        discount = validated_data.pop('discount')
        appointment = Appointment.objects.create(**validated_data)

        self.get_or_create_branch(branch, appointment)
        self.get_or_create_client(client, appointment)
        self.get_or_create_technician(technician, appointment)
        self.get_or_create_service(service, appointment)
        self.get_or_create_payment(payment, appointment)
        self.get_or_create_discount(discount, appointment)

        return appointment

    def update(self, instance, validated_data):
        """Update appointment."""
        branch = validated_data.pop('branch')
        client = validated_data.pop('client')
        technician = validated_data.pop('technician')
        service = validated_data.pop('service')
        payment = validated_data.pop('payment')
        discount = validated_data.pop('discount')

        if branch is not None:
            instance.branch.clear()
            self.get_or_create_branch(branch, instance)

        if client is not None:
            instance.client.clear()
            self.get_or_create_client(client, instance)

        if technician is not None:
            instance.technician.clear()
            self.get_or_create_technician(technician, instance)

        if service is not None:
            instance.service.clear()
            self.get_or_create_service(service, instance)

        if payment is not None:
            instance.payment.clear()
            self.get_or_create_payment(payment, instance)

        if discount is not None:
            instance.discount.clear()
            self.get_or_create_discount(discount, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
