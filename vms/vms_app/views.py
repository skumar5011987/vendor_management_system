from .models import (Vendor, PurchaseOrder, HistoricalPerformance)
from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import vender_serializer
from rest_framework.permissions import IsAuthenticated
from vms_app.utils import (get_po_number, parse_date, total_quantity, get_instance)
from django.utils import timezone
import logging

_logger = logging.getLogger(__name__)

class VendorsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            qs = Vendor.objects.filter(id=id)
        else:
            qs = Vendor.objects.all()
        serializer = vender_serializer.VendorSerializer(qs, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        request.data.update({'user':user.id})
        serializer = vender_serializer.VendorSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, id):
        vendor = get_instance(Vendor, id)
        if vendor:
            serializer = vender_serializer.VendorSerializer(vendor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, id):
        vendor = get_instance(Vendor, id)
        if vendor:
            vendor.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


# purchase order view
class PurchaseOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        data = self.add_params(data)
        data.update({'vendor':request.user.id})
        serializer = vender_serializer.PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, po_id=None):
        
        try:
            params = request.GET.copy()
            if po_id:
                pos = PurchaseOrder.objects.filter(id=po_id)
            else:
                if params.get('status'):
                    pos = PurchaseOrder.objects.filter(status=status)
                else:
                    pos = PurchaseOrder.objects.all()
            
            # filter by vendor
            if params.get('vender','').strip():
                vender = params.get('vender','').strip()
                pos = pos.filter(vender=vender)
            
            serializer = vender_serializer.PurchaseOrderSerializer(pos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exc:
            print(f"Error:{exc}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, po_id):
        try:
            data = request.data        
            # parse date
            if 'delivery_date' in data:
                data.update({'delivery_date':parse_date(data.get('delivery_date'))})
            
            user = request.user
            data.update({'user':user})
            po = get_instance(PurchaseOrder, po_id)
            if po and po.status=='pending':
                serializer = vender_serializer.PurchaseOrderSerializer(po, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            print(f"Something went wrong.")
    
    def delete(self, request, po_id):
        po = get_instance(PurchaseOrder, po_id)
        if po:
            po.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    def add_params(self, data):
        po_number = get_po_number()
        delivery_date = parse_date(data.get('delivery_date'))
        quantity = total_quantity(data.get('items'))
        data.update({
            'po_number':po_number,
            'delivery_date':delivery_date,
            'quantity': quantity,
            'issue_date': timezone.now() 
            })
        return data


class AcknowledgePOAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, po_id):        
        po = get_instance(PurchaseOrder, po_id)
        if po:
            data = {'acknowledgment_date': timezone.now()}
            serializer = vender_serializer.PurchaseOrderSerializer(
                po, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class VendorsPerformanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        vendor = Vendor.objects.get(id=id)
        if vendor:
            serializer = vender_serializer.VendorPerformanceSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
