from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, HistoricalPerformance
from django.db.models import Avg
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def calculate_performance(sender, instance, created, **kwargs):
    if not created:
        if instance.status=='completed':
            now = timezone.now()
            vendor = instance.vendor
            pos = PurchaseOrder.objects.filter(vendor = vendor)
            total_pos = pos.count()
            completed_count = pos.filter(status='completed').count()
            completed_before = pos.filter(status='completed', delivery_date__gte=now).count()
            
            # on_time_delivery_rate
            vendor.on_time_delivery_rate = completed_count / completed_before
            
            # Quality Rating Average
            qty_rating_avg = PurchaseOrder.objects.aggregate(avg_value=Avg('quality_rating'))
            avg_rating = qty_rating_avg['avg_value']
            if avg_rating is not None:
                vendor.quality_rating_avg = avg_rating
            
            # Fulfilment Rate
            vendor.fulfillment_rate = total_pos / completed_count
            
            # Average Response Time
            
            vendor.save()