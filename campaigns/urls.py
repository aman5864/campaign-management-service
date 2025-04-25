from django.urls import path
from .views import CampaignListCreateAPIView, CampaignDetailAPIView, AvailableCampaignAPIView

urlpatterns = [
    path('campaigns/', CampaignListCreateAPIView.as_view(), name='campaign-list'),
    path('campaigns/<int:pk>/', CampaignDetailAPIView.as_view(), name='campaign-detail'),
    path('campaigns/available/', AvailableCampaignAPIView.as_view(), name='campaign-available'),
]

