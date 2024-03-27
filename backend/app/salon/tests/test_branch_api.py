"""
Tests for branch APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Branch
)

from salon.serializers import BranchSerializer


BRANCHES_URL = reverse('salon:branch-list')


def create_branch(**params):
    """Create and return a sample branch."""
    defaults = {
        'name': 'Sample branch name',
        'address': 'Sample branch address',
        'start_time': '08:00:00',
        'end_time': '17:00:00',
    }
    defaults.update(params)

    branch = Branch.objects.create(**defaults)
    return branch


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicBranchAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BRANCHES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBranchApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_branchs(self):
        """Test retrieving a list of branchs."""
        create_branch()
        create_branch()

        res = self.client.get(BRANCHES_URL)

        branches = Branch.objects.all()
        serializer = BranchSerializer(branches, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_branch(self):
        """Test creating a branch."""
        payload = {
            'name': 'Sample branch',
            'address': 'Sample adddress branch',
            'start_time': '08:00:00',
            'end_time': '19:00:00',
        }
        res = self.client.post(BRANCHES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_partial_update(self):
        """Test updating a branch."""
        branch = create_branch()
        payload = {
            'name': 'Updated branch name',
        }
        url = reverse('salon:branch-detail', args=[branch.id])
        res = self.client.patch(url, payload)

        branch.refresh_from_db()
        self.assertEqual(branch.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_full_update(self):
        """Test updating a branch."""
        branch = create_branch()
        payload = {
            'name': 'Updated branch name',
            'address': 'Updated branch address',
            'start_time': '08:00:00',
            'end_time': '19:00:00',
        }
        url = reverse('salon:branch-detail', args=[branch.id])
        res = self.client.put(url, payload)

        branch.refresh_from_db()
        self.assertEqual(branch.name, payload['name'])
        self.assertEqual(branch.address, payload['address'])
        self.assertEqual(str(branch.start_time), payload['start_time'])
        self.assertEqual(str(branch.end_time), payload['end_time'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_branch(self):
        """Test deleting a branch successful."""
        branch = create_branch()
        url = reverse('salon:branch-detail', args=[branch.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Branch.objects.filter(id=branch.id).exists())
