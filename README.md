# Django Developer Assignment
# Vendor Management System with Performance Metrics 
Author: Sailesh kumar

# Objective
Develop a Vendor Management Systemusing Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics.

# Core Features
1. Vendor Profile Management
2. Purchase Order Tracking
3. Vendor Performance Evaluation

# Prerequisites
Before you start, make sure you have the following prerequisites installed on your system:

1. Python 3.9
3. virtualenv
4. pip (Python package manager)

# Installation/Project setup
1. Create a folder and open in editor (VSCode).
2. Open new terminal
3. Create a virtual environment to isolate project dependencies.
    virtualenv venv
4. Activate the virtual environment.
    source venv/bin/activate(for linux) Or venv/Scripts/activate(for windos)
5. Clone the project (git clone https://github.com/skumar5011987/vendor_management_system.git)
7. Move to the project directory containing file 'requirements.py'
    say: cd /vms
8. Install project dependencies from the requirements.txt file.
    pip install -r requirements.txt
9. Makesure there should be postgresql & pgAdmin installed and listning apt port: 5432
10. Create a database
11. open settings.py file and update DATABASE setting.
    ex: DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': DB_NAME,
                'USER': DB_USER,
                'PASSWORD': DB_PASS,
                'HOST': DB_HOST,
                'PORT': DB_PORT,
            },
        }
12. Run Migration and migrate to create database schema.
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver

13. Cerate a super user
    python manage.py createsuper user

14. Get Authentication token save it to use in api calls.
    python manage.py drf_create_token <username>
    Ex: token 5bbc73193b1e9f4d5b82bb004aac31c008b2514a (this is need to added as Authorization in api call)

# API Endpoints
1. Create new Vendor
    URL: http://localhost:8000/api/vendors/
    Method: POST
    Ex. data: {
        "name":"Pinogy Corporation",
        "contact_details": "9999999999",
        "address": "abc-202 Noida"
    }
    Description: Creates new vendor and return the vendor info in response.

2. List all vendors.
    URL: http://localhost:8000/api/vendors/
    Method: GET
    Description: Returns the list of all vendors in response.

3. Retrieve a specific vendor's details.
    URL: http://localhost:8000/api/vendors/{condor_id}/
    Method: GET
    Description: Returns the vendor in response if found otherwise returns blank list.

4. Update a vendor's details.
    URL: http://localhost:8000/api/vendors/{vondor_id}/
    Method: PUT
    Ex. data : {    
        "contact_details": "2345556788",
        "address": "abc-235 Noida"
    }
    Description: Update the vendor details and return the updated vendor details.

5. Delete a vendor.
    URL: http://localhost:8000/api/vendors/{vondor_id}/
    Method: DELETE
    Description: Deletes the vendor if exists.

6. Create a purchase order.
    URL: http://localhost:8000/api/purchase_orders/
    Method: POST
    Ex. data : {
        "vendor": 3,
        "items":{
            "Parle g": 270,
            "Good day": 240
            }
    }
    Description: Creates new Purchase order and return the order in response.

7. List all purchase orders with an option to filter by vendor.
 URL: http://localhost:8000/api/purchase_orders/
    Method: GET
    Description: Returns the list of all Purchase orders in response.

    URL: http://localhost:8000/api/purchase_orders/?vender=3
    Method: GET
    Description: Returns the list of all Purchase orders in response where vendor = 3.

8. Retrieve details of a specific purchase order.
    URL: http://localhost:8000/api/purchase_orders/{po_id}/
    Method: GET
    Description: Returns the Purchase order in response where purchase order id = {po_id}.

9. Update a purchase order.
    URL: http://localhost:8000/api/purchase_orders/{po_id}/
    Method: PUT
    Ex. data : {    
        "items":{
            "Parle g": 290,
            "Good day": 280
            },
        "delivery_date": "25-12-2023" (date format DD/MM/YYYY)
}
    Description: Update the Purchase order details and return the updated Purchase order.

10. Delete a purchase order.
    URL: http://localhost:8000/api/purchase_orders/{po_id}/
    Method: DELETE
    Description: Deletes the  Purchase order if exists.

11. 