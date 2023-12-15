
from django.contrib.auth.models import User
from vms_app.models import Vendor, PurchaseOrder
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

class ModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='api_user', password='testpassword')
        self.client.force_authenticate(user=self.user)
        # print(self.client)
        vals = {
                "name": "Pet Land",
                "contact_details": "1111111111",
                "address": "ASD-002 Noida"
            }
        
        # create vendor
        self.vendor = Vendor.objects.create(**vals)
        
        order_data = {
            "vendor": self.vendor,
            "items":{
            "Parle g": 270,
            "Good day": 240,
            },
            "delivery_date": "2023-12-30" # (date format YYYY-MM-DD) [it is optional, if not provided it will assign date after 7 day]
            }
        
        # create purchase order
        self.po = PurchaseOrder.objects.create(**order_data)
        self.po.po_number = 'E8AFB11C2866'
        self.po.issue_date = timezone.now()
        self.po.acknowledgment_date = timezone.now()+timedelta(days=1)
        self.po.save()
    
    def test_create_vendor(self):
        """create vendor testcase""" 
        
        url = reverse('vendors') 
        data = {
            "name": "Lucky Puppy",
            "contact_details": "9999999000",
            "address": "abc-222 Delhi",
            "user": self.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_vendors(self):
        """List all vendors and get vendor by ID """
        
        url = reverse('vendors') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # get vendor by id
        url = reverse('vendor', kwargs={'id': self.vendor.id}) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_vendor(self):
        """Update vendor details"""
        
        url = reverse(f'vendor', kwargs={'id': self.vendor.id})
        data = {
            "name": "Lucky Puppy Updated",
            "contact_details": "9999999001",
            "address": "abc-222 South Delhi",
            "user": self.user.id
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_vendor(self):
        """Delete vendor by id."""
        
        url = reverse('vendor', kwargs={'id': self.vendor.id}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        """Create Purchase Order"""
        
        data = {
            "vendor": self.vendor.pk,
            "items":{
            "Item_1": 270,
            "Item_2": 240,
            },
            "delivery_date": "2024-05-01"
            }
        url = reverse(f'purchase_orders')
        response = self.client.post(url, data, format="json",)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_pos(self):
        """Get Purchase orders"""
        
        url = reverse('purchase_orders')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_acknowledgment_and_po(self):
        """Acknowledge the purchase Order """
        
        url = reverse('acknowledge', kwargs = {'po_id':self.po.pk})
        
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_po(self):
        """Update Purchase Order"""
        data={
            'status': 'completed',
            'quality_rating':89
        }
        
        url = reverse('purchase_order', kwargs={'po_id':self.po.pk})
        response = self.client.put(url, data, format="json",)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_po(self):
        """Delete Purchase Order"""
        
        url = reverse('purchase_order', kwargs={'po_id':self.po.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_vendor_performance(self):
        """Get Vendor Performance"""
        
        url = reverse('vendors_performance', kwargs={'id':self.vendor.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        