from django.db import models
from django.utils import timezone

DISCOUNT_TYPE_CHOICES = [
    ('cart', 'Cart'),
    ('delivery', 'Delivery'),
]


class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField(max_length=255, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    usage_limit_per_customer_per_day = models.IntegerField()
    target_customers = models.ManyToManyField(Customer, through='CampaignCustomer')

    total_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.total_spent < self.budget


class CampaignCustomer(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('campaign', 'customer')


class CampaignUsageLog(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    usage_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('campaign', 'customer', 'date')

