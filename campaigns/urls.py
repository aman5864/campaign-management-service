from django.urls import path
from .views import CampaignListCreateAPIView, CampaignDetailAPIView, AvailableCampaignAPIView, \
    CustomerListCreateAPIView, CustomerDetailAPIView, ApplyDiscountView

urlpatterns = [
    path('campaigns', CampaignListCreateAPIView.as_view(), name='campaign-list'),
    path('campaigns/<int:pk>', CampaignDetailAPIView.as_view(), name='campaign-detail'),
    path('campaigns/available', AvailableCampaignAPIView.as_view(), name='campaign-available'),
    path('customers', CustomerListCreateAPIView.as_view(), name='customer-list'),
    path('customers/<int:pk>', CustomerDetailAPIView.as_view(), name='customer-detail'),
    path('campaigns/<int:campaign_id>/apply-discount', ApplyDiscountView.as_view(), name='apply-discount'),
]

