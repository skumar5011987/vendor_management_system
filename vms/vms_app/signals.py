from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.db.models import Avg
from django.utils import timezone
import logging

_logger = logging.getLogger(__name__)

@receiver(post_save, sender=PurchaseOrder)
def calculate_performance(sender, instance, created, **kwargs):
    if not created:
        if instance.status=='completed':
            try:
                now = timezone.now()
                vendor = instance.vendor
                pos = PurchaseOrder.objects.filter(vendor = vendor)
                total_pos = pos.count()
                completed_count = pos.filter(status='completed').count()
                completed_before = pos.filter(status='completed', delivery_date__gte=now).count()
                
                # on_time_delivery_rate
                vendor.on_time_delivery_rate = round((completed_count // completed_before),2) * 100
                
                # Quality Rating Average
                qty_rating_avg = pos.filter(status='completed').aggregate(avg_value=Avg('quality_rating'))
                avg_rating = round(qty_rating_avg['avg_value'], 2)
                
                # Fulfilment Rate
                vendor.fulfillment_rate = round(completed_count / total_pos, 2) * 100
                # Average Response Time
                instance.avg_resp_time(avg_rating)
                # vendor.save()
            except Exception as exc:
                _logger.error(f"Can't update vendor metrics. Error : {exc}")

@receiver(post_save, sender=PurchaseOrder)
def recalculate_avg_res_time(sender, instance, created, **kwargs):
    if not created:
        instance.avg_resp_time(update=True)
        
@receiver(post_save, sender=Vendor)
def create_purchase_history(sender, instance, created, **kwargs):
    if not created:
        try:
            values = {
                'on_time_delivery_rate': instance.on_time_delivery_rate,
                'quality_rating_avg': instance.quality_rating_avg,
                'average_response_time': instance.average_response_time,
                'fulfillment_rate': instance.fulfillment_rate
            }
            HistoricalPerformance.objects.create(vendor=instance, **values)
        except Exception as exc:
            _logger.error(f"Can't create historical performance. Error: {exc}")