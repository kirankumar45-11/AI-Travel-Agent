AI Travel Agent

AI Travel Agent is a full-stack travel planning web application developed using Django, HTML, CSS, and JavaScript. The application helps users discover destinations, generate travel itineraries, manage bookings, estimate budgets, and organize trips through a clean and responsive interface.

Features
  User Authentication System
    Registration
    Login & Logout
    Session Management
  AI Travel Planner
    Smart itinerary generation
    Destination recommendations
    Budget planning
  Hotel Recommendation System
    Hotel listings
    Pricing and details
    Booking support
  Saved Trips
    Save and manage travel plans
    Recently visited places
  Payment Module
    Simulated payment system
    Booking confirmation
  Invoice Generation
    Trip summary
    Printable invoice page
  Responsive UI
    Mobile-friendly design
    Modern travel-themed interface

    Technology Stack
Backend
  Python
  Django
Frontend
  HTML
  CSS
  JavaScript
Database
  SQLite

Project Structure
  AI-Travell-Agent/
  │
  ├── manage.py
  ├── db.sqlite3
  ├── media/
  ├── static/
  ├── templates/
  ├── travel_agent_project/
  ├── travel_app/
  └── requirements.txt

Installation & Setup
  1. Clone Repository
    git clone https://github.com/your-username/AI-Travell-Agent.git
    cd AI-Travell-Agent
  2. Create Virtual Environment
    Windows
    python -m venv venv
    venv\Scripts\activate
  Linux / Mac
    python3 -m venv venv
    source venv/bin/activate
  3. Install Dependencies
    pip install -r requirements.txt
  4. Apply Migrations
    python manage.py makemigrations
    python manage.py migrate
  5. Run Server
    python manage.py runserver

Open browser:
  http://127.0.0.1:8000/

Main Modules
  Authentication Module
      User registration
      Login/logout
      Profile management
  Travel Planner Module
      Destination search
      AI itinerary generation
      Budget estimation
  Booking Module
      Hotel booking
      Trip management
  Payment Module
      Payment simulation
      Booking confirmation
  Invoice Module
      Generate trip invoice
      Printable bill


Database Models
  User
  UserProfile
  Trip
  Hotel
  Payment
  SavedTrip
  RecentPlace

Admin Panel
  To access Django admin panel:
      http://127.0.0.1:8000/admin
Create superuser:
      python manage.py createsuperuser

Future Improvements
  AI chatbot assistant
  Weather API integration
  Google Maps integration
  Real payment gateway
  Email notifications
  PDF invoice download

Screenshots
  Add project screenshots here.
  Example:
      Home Page
      Dashboard
      Planner Page
      Payment Page
      Invoice Page

Learning Outcomes
  This project demonstrates:
      Full-stack web development
      Django backend development
      Database management
      Responsive frontend design
      Authentication systems
      Travel management workflow

Author
R Kiran Kumar
Computer Science and Engineering
Kishkinda University
