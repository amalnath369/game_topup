# Top-Up API Django Project

A Django-based web application to manage top-up product orders for various games.

## Features

- Game and Product Models
- Top-up Order API with validation
- Analytics Dashboard (Top 5 products, Revenue, Failed payments)
- Admin panel for staff users

## Setup Instructions

1. Clone the repository:

   git clone https://github.com/amalnath369/game_topup  
   cd game_topup

2. Create a virtual environment:

   python -m venv venv  
   venv\Scripts\activate   (on Windows)  
   or  
   source venv/bin/activate   (on macOS/Linux)

3. Install dependencies:

   pip install -r requirements.txt

4. Apply migrations:

   python manage.py migrate

5. Create a superuser:

   python manage.py createsuperuser

6. Run the server:

   python manage.py runserver

## API Endpoint

POST /api/topup/  
Submit a new top-up order.

Sample JSON body:

{
  "gamename": "PUBG Mobile",
  "game_id": "pubg001",
  "product_name": "UC Pack 500",
  "product_id": 1,
  "product_price": 449.00,
  "user_email": "user@example.com",
  "payment_status": "success"
}

## Admin Analytics

Visit: http://127.0.0.1:8000/dashboard/ (Login as staff)

Includes:
- Top 5 most purchased products
- Revenue over last 7 days
- Failed payments this month
