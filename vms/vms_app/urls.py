from django.urls import path
from vms_app.views import *

urlpatterns = [
    path('vendors/', VendorsAPIView.as_view(), name='vendors'),
    path('vendors/<int:id>/', VendorsAPIView.as_view(), name='vendor'),
    path('purchase_orders/', PurchaseOrderAPIView.as_view(), name='purchase_orders'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderAPIView.as_view(), name='purchase_order'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePOAPIView.as_view(), name='acknowledge'),
    path('vendors/<int:id>/performance/', VendorsPerformanceAPIView.as_view(), name='vendors_performance'),
    path('vendors/<int:id>/performancehistory/', VendorsPerformanceHistoryAPIView.as_view(), name='vendors_performance_history')
]