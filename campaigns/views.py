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
        cart_total = float(request.query_params.get('cart_total', 0))
        delivery_fee = float(request.query_params.get('delivery_fee', 0))

        if not customer_id:
            return Response({'error': 'customer_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customer, pk=customer_id)
        available_campaigns = []

        for campaign in Campaign.objects.filter(target_customers=customer):
            if is_campaign_active(campaign) and not has_exceeded_usage(campaign, customer):
                if campaign.discount_type == 'cart' and cart_total >= campaign.discount_amount:
                    available_campaigns.append(campaign)
                elif campaign.discount_type == 'delivery' and delivery_fee >= campaign.discount_amount:
                    available_campaigns.append(campaign)

        serializer = CampaignSerializer(available_campaigns, many=True)
        return Response(serializer.data)
