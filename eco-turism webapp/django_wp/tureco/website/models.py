from django.db import models
from django.contrib.auth.models import User as AUser
from datetime import datetime
from django.core.validators import MinValueValidator

# Create your models here.
class User(models.Model):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('hotel_manager', 'Hotel Manager'),
        ('transport_manager', 'Transport Manager'),
    )
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    user_role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.email} ({self.get_user_role_display()})"
    
    def is_customer(self):
        return self.user_role == 'customer'
    
    def is_hotel_manager(self):
        return self.user_role == 'hotel_manager'
    
    def is_transport_manager(self):
        return self.user_role == 'transport_manager'

class Account(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    dateofbirth = models.DateField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Account of {self.fname} {self.lname}'

class Address(models.Model):
    addr1 = models.CharField(max_length=255)
    addr2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)

class TransportationTrip(models.Model):
    TRANSPORT_TYPES = (
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('flight', 'Flight'),
    )
    transport_type = models.CharField(max_length=10, choices=TRANSPORT_TYPES)
    operator_name = models.CharField(max_length=120)
    origin_city = models.CharField(max_length=120)
    destination_city = models.CharField(max_length=120)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    car_reg = models.CharField(max_length=10, unique=True)
    total_seats = models.PositiveIntegerField(default=50)
    price_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
    thumbnail_url = models.URLField(blank=True)
    manager_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_trips', limit_choices_to={'user_role': 'transport_manager'})

    def __str__(self):
        return f"{self.get_transport_type_display()} {self.origin_city}→{self.destination_city} ({self.departure:%Y-%m-%d %H:%M})"

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(blank=True)
    tags = models.CharField(max_length=50, blank=True)
    manager_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_hotels', limit_choices_to={'user_role': 'hotel_manager'})

    def __str__(self):
        return f"{self.name} — {self.city}"

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    name = models.CharField(max_length=120)
    max_persons = models.PositiveIntegerField(default=2)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    total_rooms = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} @ {self.hotel.name}"

class Review(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField(max_length=1000, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=1)
    eco_rating = models.PositiveSmallIntegerField(default=1)
    create_at = models.DateTimeField(auto_now_add=True)
    hotel_id = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="reviews")
    staff_user = models.ForeignKey(
        AUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_hotel_reviews"
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    class Meta:
        ordering = ["-create_at"]

    def __str__(self):
        user_display = f"{self.account_id.fname} {self.account_id.lname}" if self.account_id else "Anonymous"
        return f"Review for {self.hotel_id.name} by {user_display}"

    @property
    def is_reply(self):
        return self.parent_id is not None

class RoomBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room_type = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_nr = models.PositiveIntegerField(unique=True, null=True, blank=True)
    check_in = models.DateField()
    check_out = models.DateField()
    room_booked = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Guest booking fields
    guest_name = models.CharField(max_length=200, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        if self.is_guest:
            return f"Guest Booking #{self.id} by {self.guest_name or 'Guest'}"
        return f"Room Booking #{self.id} by {self.user.email if self.user else 'Unknown'}"

class TripBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    trip = models.ForeignKey(TransportationTrip, on_delete=models.CASCADE)
    booking_nr = models.PositiveIntegerField(unique=True, null=True, blank=True)
    seats_booked = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Guest booking fields
    guest_name = models.CharField(max_length=200, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    guest_phone = models.CharField(max_length=20, blank=True, null=True)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        if self.is_guest:
            return f"Guest Trip Booking #{self.id} by {self.guest_name or 'Guest'}"
        return f"Trip Booking #{self.id} by {self.user.email if self.user else 'Unknown'}"
