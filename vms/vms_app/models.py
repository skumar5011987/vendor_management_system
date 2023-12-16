from django.contrib.auth.models import User
from datetime import timedelta
from django.db import models
import uuid

# vender model
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField(blank=True)
    vendor_code = models.CharField(max_length=50, unique=True, blank=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.vendor_code:
            unique_code = str(uuid.uuid4().hex[:8]).upper()
            while Vendor.objects.filter(vendor_code=unique_code).exists():
                unique_code = str(uuid.uuid4().hex[:8]).upper()
            
            self.vendor_code = unique_code
        super(Vendor, self).save(*args, **kwargs)
            


# purchase oder model
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name='vendor')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO Number: {self.po_number} - Vendor: {self.vendor.name}"
    
    def avg_resp_time(self, **kwargs):
        vendor = self.vendor
        
        all_po = PurchaseOrder.objects.filter(vendor=vendor).exclude(status='canceled')
        td_list = []
        for obj in all_po:
            if obj.acknowledgment_date:
                td_list.append(obj.acknowledgment_date - obj.issue_date)
        total_timedelta = sum(td_list, timedelta(0))
        if td_list:
            td = total_timedelta / len(td_list)
        
        return (td.days*24 + td.seconds // 3600)
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE, related_name = 'vendor_history')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True,null=True)

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"