from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class Trip(models.Model):
    TRAVEL_TYPES = [
        ('Solo', 'Solo'),
        ('Family', 'Family'),
        ('Adventure', 'Adventure'),
        ('Romantic', 'Romantic'),
        ('Business', 'Business'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    starting_point = models.CharField(max_length=200, default='Delhi')
    destination_name = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    travel_type = models.CharField(max_length=50, choices=TRAVEL_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def duration(self):
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"{self.destination_name} trip for {self.user.username}"

class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField()
    activities = models.TextField()
    meals = models.TextField(blank=True)
    expenses_estimate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['day_number']

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    amenities = models.TextField(blank=True)

    def __str__(self):
        return self.name

class SavedTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_data = models.JSONField() # Stores serialized trip info
    saved_at = models.DateTimeField(auto_now_add=True)

class RecentPlace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=200)
    visited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-visited_at']

class Payment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Success')
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.trip.destination_name}"
