"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_non_staff_user(self):
        """Test creating a non-staff user."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertFalse(user.is_staff)

    def test_create_technician(self):
        """Test creating a technician user."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        technician = models.Technician.objects.get(user=user)

        self.assertTrue(user.is_staff)
        self.assertEqual(technician.user, user)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertFalse(user.is_staff)

    # def test_create_branch(self):
    #     """Test creating a branch is successful."""

    #     branch = models.Branch.objects.create(
    #         name='Sample branch name',
    #         address='Sample branch address',
    #         start_time='08:00:00',
    #         end_time='17:00:00',
    #     )

    #     self.assertEqual(str(branch), branch.name)

    # def test_create_skill(self):
    #     """Test creating a skill is successful."""

    #     skill = models.Skill.objects.create(
    #         name='Sample skill name',
    #     )

    #     self.assertEqual(str(skill), skill.name)

    # def test_update_technician_fields(self):
    #     """Test updating technician fields (skills and branches)."""

    #     user = get_user_model().objects.create_user('test_update@example.com',
    #                                                 'test123')
    #     technician = models.Technician.objects.get(user=user)

    #     # Create sample skills and branches
    #     skill1 = models.Skill.objects.create(name='Skill 1')
    #     skill2 = models.Skill.objects.create(name='Skill 2')
    #     branch1 = models.Branch.objects.create(name='Branch 1')
    #     branch2 = models.Branch.objects.create(name='Branch 2')

    #     # Add skills and branches to technician
    #     technician.skills.add(skill1)
    #     technician.skills.add(skill2)
    #     technician.branches.add(branch1)
    #     technician.branches.add(branch2)

    #     # Update skills and branches
    #     new_skill = models.Skill.objects.create(name='New Skill')
    #     new_branch = models.Branch.objects.create(name='New Branch')

    #     technician.skills.add(new_skill)
    #     technician.branches.add(new_branch)

    #     # Assert that the technician's skills and branches have been updated
    #     self.assertIn(skill1, technician.skills.all())
    #     self.assertIn(skill2, technician.skills.all())
    #     self.assertIn(new_skill, technician.skills.all())
    #     self.assertIn(branch1, technician.branches.all())
    #     self.assertIn(branch2, technician.branches.all())
    #     self.assertIn(new_branch, technician.branches.all())

    # def test_create_service(self):
    #     """Test creating a service is successful."""

    #     service = models.Service.objects.create(
    #         name='Sample service name',
    #         price=100.00,
    #     )

    #     self.assertEqual(str(service), service.name)
    #     self.assertEqual(service.price, service.price)

    # def test_create_payment(self):
    #     """Test creating a payment is successful."""

    #     payment = models.Payment.objects.create(
    #         format_code='02',
    #         description='Sample payment description',
    #     )

    #     self.assertEqual(str(payment), payment.description)

    # def test_create_discount(self):
    #     """Test creating a discount is successful."""

    #     discount = models.Discount.objects.create(
    #         description='Sample discount description',
    #         value=10.00,
    #     )

    #     self.assertEqual(str(discount), discount.description)

    # def test_create_promo(self):
    #     """Test creating a promo is successful."""

    #     promo = models.Promo.objects.create(
    #         weekday=1,
    #         name='Sample promo name',
    #     )

    #     self.assertEqual(str(promo), promo.name)

    # def test_create_client(self):
    #     """Test creating a client is successful."""

    #     client = models.Client.objects.create(
    #         name='John',
    #         last_name='Doe 2.0',
    #         phone='1234567890',
    #         email='john.doe2@example.com',
    #         birthday='1990-01-01',
    #         comments='Sample comments',
    #     )

    #     self.assertEqual(str(client), f"{client.name} {client.last_name}")
    #     self.assertEqual(client.phone, '1234567890')
    #     self.assertEqual(client.email, 'john.doe2@example.com')
    #     self.assertEqual(client.birthday, '1990-01-01')
    #     self.assertEqual(client.comments, 'Sample comments')

    # def test_create_appointment(self):
    #     """Test creating an appointment is successful."""

    #     user = create_user(email='user_appointment@example.com',
    #                        password='test123')
    #     technician = models.Technician.objects.get(user=user)
    #     client = models.Client.objects.create(
    #         name='John',
    #         last_name='Doe',
    #         phone='1234567890',
    #         email='john.doe@example.com',
    #         birthday='1990-01-01',
    #         comments='Sample comments',
    #     )
    #     branch = models.Branch.objects.create(
    #         name='Sample branch name',
    #         address='Sample branch address',
    #         start_time='08:00:00',
    #         end_time='17:00:00',
    #     )
    #     service = models.Service.objects.create(
    #         name='Sample service name',
    #         price=100.00,
    #     )
    #     appointment = models.Appointment.objects.create(
    #         technician=technician,
    #         branch=branch,
    #         service=service,
    #         client=client,
    #         date='2021-01-01',
    #         time='08:00:00',
    #     )

    #     self.assertEqual(
    #         str(appointment), f'{appointment.date} - {appointment.time} - {appointment.client}'
    #     )
    #     self.assertEqual(appointment.technician, technician)
    #     self.assertEqual(appointment.branch, branch)
    #     self.assertEqual(appointment.service, service)
    #     self.assertEqual(appointment.client, client)
    #     self.assertEqual(appointment.date, '2021-01-01')
    #     self.assertEqual(appointment.time, '08:00:00')
    #     self.assertFalse(appointment.warranty)
