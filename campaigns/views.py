from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Campaign, Customer, CampaignUsageLog
from .serializers import CampaignSerializer, CustomerSerializer


def is_campaign_active(campaign):
    now = timezone.now()
    return campaign.start_date <= now <= campaign.end_date and campaign.total_spent < campaign.budget


def has_exceeded_usage(campaign, customer):
    today = timezone.now().date()
    usage_log = CampaignUsageLog.objects.filter(
        campaign=campaign,
        customer=customer,
        date=today
    ).first()
    return usage_log and usage_log.usage_count >= campaign.usage_limit_per_customer_per_day


def is_valid_campaign(campaign, customer, cart_total, delivery_fee):
    today = timezone.now().date()
    if not is_campaign_active(campaign):
        return False
    usage_log = CampaignUsageLog.objects.filter(
        campaign=campaign, customer=customer, date=today
    ).first()
    if usage_log and usage_log.usage_count >= campaign.usage_limit_per_customer_per_day:
        return False
    if campaign.discount_type == 'cart' and cart_total >= campaign.discount_amount:
        return True
    if campaign.discount_type == 'delivery' and delivery_fee >= campaign.discount_amount:
        return True
    return False


class CampaignListCreateAPIView(APIView):

    def get(self, request):
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            campaign = serializer.save()
            return Response(CampaignSerializer(campaign).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CampaignDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Campaign, pk=pk)

    def get(self, request, pk):
        campaign = self.get_object(pk)
        serializer = CampaignSerializer(campaign)
        return Response(serializer.data)

    def put(self, request, pk):
        campaign = self.get_object(pk)
        serializer = CampaignSerializer(campaign, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        campaign = self.get_object(pk)
        campaign.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailableCampaignAPIView(APIView):

    def get(self, request):
        customer_id = request.query_params.get('customer_id')
        try:
            cart_total = float(request.query_params.get('cart_total', 0))
            delivery_fee = float(request.query_params.get('delivery_fee', 0))
        except ValueError:
            return Response({'error': 'cart_total and delivery_fee must be numbers'}, status=status.HTTP_400_BAD_REQUEST)

        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customer, pk=customer_id)
        campaigns = Campaign.objects.prefetch_related('target_customers').filter(target_customers=customer)

        valid_campaigns = [campaign for campaign in campaigns
                           if is_valid_campaign(campaign, customer, cart_total, delivery_fee)]
        serializer = CampaignSerializer(valid_campaigns, many=True)
        return Response(serializer.data)
