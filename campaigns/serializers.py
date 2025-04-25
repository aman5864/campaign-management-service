from rest_framework import serializers
from .models import Campaign, Customer, CampaignCustomer, CampaignUsageLog


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    target_customers = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Customer.objects.all()
    )

    class Meta:
        model = Campaign
        fields = '__all__'


class CampaignCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCustomer
        fields = '__all__'


class CampaignUsageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignUsageLog
        fields = '__all__'
