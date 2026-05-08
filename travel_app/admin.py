from django.contrib import admin
from .models import UserProfile, Destination, Trip, Itinerary, Hotel, SavedTrip, RecentPlace, Payment

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'rating')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination_name', 'travel_type', 'start_date', 'end_date')

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('trip', 'day_number')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'price_per_night', 'rating')

@admin.register(SavedTrip)
class SavedTripAdmin(admin.ModelAdmin):
    list_display = ('user', 'saved_at')

@admin.register(RecentPlace)
class RecentPlaceAdmin(admin.ModelAdmin):
    list_display = ('user', 'place_name', 'visited_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'trip', 'amount', 'status')
