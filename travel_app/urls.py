from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('planner/', views.ai_planner, name='ai_planner'),
    path('itinerary/<int:trip_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('hotels/', views.hotel_recommendations, name='hotels'),
    path('hotels/<int:trip_id>/', views.hotel_recommendations, name='hotels_with_trip'),
    path('payment/<int:trip_id>/', views.payment_view, name='payment'),
    path('invoice/<int:trip_id>/', views.invoice_view, name='invoice'),
    path('saved-trips/', views.saved_trips, name='saved_trips'),
    path('save-trip/<int:trip_id>/', views.save_trip_toggle, name='save_trip_toggle'),
    path('saved-items/', views.saved_items_view, name='saved_items'),
    path('destinations/', views.destinations_view, name='destinations'),
    path('profile/', views.profile_view, name='profile'),
    path('discover/', views.discover_view, name='discover'),
    path('seasonal-guide/', views.seasonal_guide, name='seasonal_guide'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('destinations/delete/<str:destination_name>/', views.delete_destination, name='delete_destination'),
    path('discover/api/', views.discovery_bot_api, name='discovery_bot_api'),
]
