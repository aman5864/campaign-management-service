# Campaign Management Service

A backend service built with Django and Django REST Framework for managing discount campaigns with customer targeting, usage limits, and budget constraints.

---

## Features

- Create, update, delete discount campaigns
- Set constraints: duration, total budget, daily usage per user
- Target specific customers for each campaign
- Real-time campaign availability check based on:
  - Customer ID
  - Cart total
  - Delivery fee
- Budget tracking and usage logging
- Unit & integration test coverage included

---

## Tech Stack

- **Python 3.10+**
- **Django 4.2+**
- **Django REST Framework**
- **SQLite** (easily swappable to PostgreSQL/MySQL)

---

## Setup Instructions

1. **Clone the repository**  
   ```bash
   git clone https://github.com/aman5864/campaign-management-service.git
   cd campaign_management_service
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Linux/macOS
   venv\Scripts\activate           # On Windows
   ```
   
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
5. **Run unit and integration tests**
   ```bash
   python manage.py test
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```
   
---

## API Documentation
1. **Create Customer**
   * URL: ```/api/customers```
   * Method: ```POST```
   * Description: ```Create a new customer.```
   * Request Body: 
   ```
   {
    "email": "xyz@gmail.com",
    "name": "sample name"
   }
   ```
   * Response: ```201 CREATED```
   ```
   {
    "id": 11,
    "email": "xyz@gmail.com",
    "name": "sample name"
   }
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "email": [
        "customer with this email already exists."
    ]
   }
   ```

2. **Create Campaign**
   * URL: ```/api/campaigns```
   * Method: ```POST```
   * Description: ```Create a new discount campaign.```
   * Request Body: 
   ```
   {
    "name": "Summer Sale",
    "discount_type": "cart",
    "discount_amount": 100,
    "budget": 1000,
    "start_date": "2025-05-01",
    "end_date": "2025-05-31",
    "usage_limit_per_customer_per_day": 1,
    "target_customers": [6, 8, 9]
   }
   ```
   * Response: ```201 CREATED```
   ```
   {
    "id": 1,
    "target_customers": [
        6,
        8,
        9
    ],
    "name": "Summer Sale",
    "discount_type": "cart",
    "discount_amount": "100.00",
    "start_date": "2025-05-01T00:00:00Z",
    "end_date": "2025-05-31T00:00:00Z",
    "budget": "1000.00",
    "usage_limit_per_customer_per_day": 1,
    "total_spent": "0.00"
   }
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "name": [
        "campaign with this name already exists."
    ]
   }
   ```

3. **List All Campaigns**
   * URL: ```/api/campaigns```
   * Method: ```GET```
   * Description: ```Retrieve all campaigns.```
   * Response: ```200 OK```
   ```
   [
    {
        "id": 1,
        "target_customers": [
            6,
            8,
            9
        ],
        "name": "Summer Sale",
        "discount_type": "cart",
        "discount_amount": "100.00",
        "start_date": "2025-05-01T00:00:00Z",
        "end_date": "2025-05-31T00:00:00Z",
        "budget": "1000.00",
        "usage_limit_per_customer_per_day": 1,
        "total_spent": "0.00"
    }
   ]
   ```
   
4. **List All Customers**
   * URL: ```/api/customers```
   * Method: ```GET```
   * Description: ```Retrieve all customers.```
   * Response: ```200 OK```
   ```
   [
    {
        "id": 6,
        "email": "aman@gmail.com",
        "name": "Aman Khan"
    },
    {
        "id": 7,
        "email": "anshika@gmail.com",
        "name": "Anshika Negi"
    },
    {
        "id": 8,
        "email": "puneet@gmail.com",
        "name": "Puneet Kumar"
    },
    {
        "id": 9,
        "email": "aashi@gmail.com",
        "name": "Aashi Gupta"
    },
    {
        "id": 10,
        "email": "gaurav@gmail.com",
        "name": "Gaurav Pal"
    },
    {
        "id": 11,
        "email": "xyz@gmail.com",
        "name": "sample name"
    }
   ]
   ```
   
5. **Available Campaigns for a Customer**
   * URL: ```/api/campaigns/available```
   * Method: ```GET```
   * Query Param:
      * **customer_id** (required): The ID of the customer for whom the available campaigns are being queried.
      * **cart_total** (required): The total amount of the customer's cart. Used to determine if the customer qualifies for cart-based discounts.
      * **delivery_fee** (required): The delivery fee for the customer's order. Used to determine if the customer qualifies for delivery-based discounts.
   * Description:
      * Returns only campaigns that are:
         * Active: The current date is between the start_date and end_date of the campaign.
         * Within Budget: The campaign has not exceeded its allocated budget.
         * Not Exceeded Usage Limit: The customer has not reached the usage limit for the campaign.
         * Targeted or Open: The campaign is either open to all customers or specifically targeted to the given customer.
   * Response: ```200 OK```
   ```
   [
    {
        "id": 1,
        "target_customers": [
            6,
            8,
            9
        ],
        "name": "Summer Sale",
        "discount_type": "cart",
        "discount_amount": "100.00",
        "start_date": "2025-04-24T00:00:00Z",
        "end_date": "2025-05-31T00:00:00Z",
        "budget": "1000.00",
        "usage_limit_per_customer_per_day": 1,
        "total_spent": "0.00"
    }
   ]
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "error": "customer_id is required"
   }
   ```
   
6. **Get Campaign by ID**
   * URL: `/api/campaigns/{id}`
   * Method: `GET`
   * Description: `Retrieves details of a specific campaign by its ID.`
   * Path Param:
      * id (required): The ID of the campaign you wish to retrieve. 
   * Response: `200 OK`
   ```
   {
    "id": 1,
    "target_customers": [
        6,
        8,
        9
    ],
    "name": "Summer Sale",
    "discount_type": "cart",
    "discount_amount": "100.00",
    "start_date": "2025-04-24T00:00:00Z",
    "end_date": "2025-05-31T00:00:00Z",
    "budget": "1000.00",
    "usage_limit_per_customer_per_day": 1,
    "total_spent": "0.00"
   }
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "detail": "No Campaign matches the given query."
   }
   ```
   
7. **Update Campaign**
   * URL: `/api/campaigns/{id}`
   * Method: `PUT`
   * Description: `Updates an existing campaign by its ID.`
   * Path Param:
      * id (required): The ID of the campaign you want to update.
   * Request Body: 
   ```
   {
    "discount_type": "delivery",
    "discount_amount": "10.00",
    "usage_limit_per_customer_per_day": 2
   }
   ```
   * Response: `200 OK`
   ```
   {
    "id": 1,
    "target_customers": [
        6,
        8,
        9
    ],
    "name": "Summer Sale",
    "discount_type": "delivery",
    "discount_amount": "10.00",
    "start_date": "2025-04-24T00:00:00Z",
    "end_date": "2025-05-31T00:00:00Z",
    "budget": "1000.00",
    "usage_limit_per_customer_per_day": 2,
    "total_spent": "0.00"
   }
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "detail": "No Campaign matches the given query."
   }
   ```
   
8. **Delete Campaign**
   * URL: `/api/campaigns/{id}`
   * Method: `Delete`
   * Description: `Delete an existing campaign by its ID.`
   * Path Param:
      * id (required): The ID of the campaign you want to delete.
   * Response: `204 No Content`
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "detail": "No Campaign matches the given query."
   }
   ```
   
9. **Apply Discount**
   * URL: `/api/campaigns/{id}}/apply-discount`
   * Method: `POST`
   * Description: `Apply Discount for the user.`
   * Path Param:
      * id (required): The ID of the campaign you want to apply for the user.
   * Request Body: 
   ```
   {
    "customer_id": 6,
    "cart_total": 1000,
    "delivery_fee": 50
   }
   ```
   * Response: `200 OK`
   ```
   {
    "detail": "Discount applied successfully.",
    "discount_type": "cart",
    "discount_applied": 100.0,
    "new_cart_value": 900.0,
    "new_delivery_fee": 50
   }
   ```
   * Failure Response (Example): ```400 Bad Request```
   ```
   {
    "detail": "Discount cannot be applied. Either campaign is not active, or the conditions are not met."
   }
   ```