from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Campaign, Customer, CampaignUsageLog
from datetime import timedelta


class CampaignTests(APITestCase):

    def setUp(self):
        self.customer1 = Customer.objects.create(name="Alice", email="alice@example.com")
        self.customer2 = Customer.objects.create(name="Bob", email="bob@example.com")

        self.active_campaign = Campaign.objects.create(
            name="Test Cart Discount",
            discount_type="cart",
            discount_amount=50.0,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=3),
            budget=500.0,
            usage_limit_per_customer_per_day=2
        )
        self.active_campaign.target_customers.set([self.customer1])

    def test_create_campaign(self):
        url = reverse('campaign-list')
        data = {
            "name": "Delivery Discount",
            "discount_type": "delivery",
            "discount_amount": 30,
            "start_date": timezone.now(),
            "end_date": timezone.now() + timedelta(days=2),
            "budget": 300,
            "usage_limit_per_customer_per_day": 2,
            "target_customers": [self.customer1.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Campaign.objects.count(), 2)

    def test_list_campaigns(self):
        url = reverse('campaign-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_campaign(self):
        url = reverse('campaign-detail', args=[self.active_campaign.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.active_campaign.name)

    def test_get_available_campaign_for_valid_customer(self):
        url = reverse('campaign-available')
        response = self.client.get(url, {
            'customer_id': self.customer1.id,
            'cart_total': 200,
            'delivery_fee': 20
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_available_campaign_exceeding_daily_limit(self):
        CampaignUsageLog.objects.create(
            campaign=self.active_campaign,
            customer=self.customer1,
            date=timezone.now().date(),
            usage_count=2
        )
        url = reverse('campaign-available')
        response = self.client.get(url, {
            'customer_id': self.customer1.id,
            'cart_total': 200,
            'delivery_fee': 20
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_available_campaign_out_of_budget(self):
        self.active_campaign.total_spent = 500
        self.active_campaign.save()

        url = reverse('campaign-available')
        response = self.client.get(url, {
            'customer_id': self.customer1.id,
            'cart_total': 200,
            'delivery_fee': 20
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_non_target_customer_should_not_get_discount(self):
        url = reverse('campaign-available')
        response = self.client.get(url, {
            'customer_id': self.customer2.id,
            'cart_total': 200,
            'delivery_fee': 20
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # -------------------- Edge Cases --------------------

    def test_create_campaign_with_missing_fields(self):
        url = reverse('campaign-list')
        data = {
            "name": "Bad Campaign"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

