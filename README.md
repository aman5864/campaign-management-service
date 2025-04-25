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

