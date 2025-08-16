from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from tracker.models import ConsumptionEntry


class ModelTests(TestCase):
    def test_create_consumption_entry(self):
        user = User.objects.create_user(username='u', password='p')
        entry = ConsumptionEntry.objects.create(user=user, calories=200)
        self.assertEqual(entry.calories, 200)
        self.assertIsNone(entry.name)
        self.assertIsNone(entry.quantity_g)
        self.assertEqual(entry.date, timezone.localdate())


class AuthFlowTests(TestCase):
    def test_signup_and_login(self):
        # Sign up
        resp = self.client.post(reverse('signup'), {
            'username': 'alice',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        })
        self.assertEqual(resp.status_code, 302)
        # After signup we are logged in and redirected to dashboard
        self.assertEqual(resp.url, reverse('tracker:dashboard'))
        # Dashboard loads
        resp = self.client.get(reverse('tracker:dashboard'))
        self.assertContains(resp, 'Today:')


class EntryViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')

    def test_add_entry_and_total(self):
        self.client.login(username='u', password='p')
        today = timezone.localdate().strftime('%Y-%m-%d')
        resp = self.client.post(reverse('tracker:entry_add'), {
            'calories': 500,
            'date': today,
        })
        self.assertEqual(resp.status_code, 302)
        # Check entries list total
        resp = self.client.get(reverse('tracker:entries_list'))
        # The label 'Total:' is wrapped in <strong>, so assert on the numeric value
        self.assertContains(resp, '500 kcal')
        # Dashboard total
        resp = self.client.get(reverse('tracker:dashboard'))
        self.assertContains(resp, '500 kcal')

