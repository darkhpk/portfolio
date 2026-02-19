from django.contrib import admin
from .models import (
    User as CustomerUser,
    Account, Address,
    Hotel, Room, TransportationTrip, 
    RoomBooking, TripBooking, Review
)

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

class RoomInline(admin.TabularInline):
    model = Room
    extra = 0

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ("account_id", "rate", "eco_rate", "comment")

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "password", "created_at", "last_active")
    search_fields = ("id", "email",)
    ordering = ("created_at",)
    readonly_fields = ("created_at",)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("fname", "lname", "phone", "dateofbirth", "user_id")
    search_fields = ("fname", "lname", "phone", "user_id__email")
    list_filter = ("dateofbirth",)
    inlines = [AddressInline]
    autocomplete_fields = ("user_id",)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("addr1", "addr2", "postcode", "account_id")
    search_fields = ("addr1", "addr2", "city", "postcode", "account_id__fname", "account_id__lname")
    autocomplete_fields = ("account_id",)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "tags")
    search_fields = ("name", "city", "tags")

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "hotel", "max_persons", "price_per_night", "total_rooms")
    list_filter = ("hotel", "max_persons")
    search_fields = ("name", "hotel__name")
    autocomplete_fields = ("hotel",)

@admin.register(TransportationTrip)
class TransportationTripAdmin(admin.ModelAdmin):
    list_display = (
        "transport_type", "operator_name", "origin_city", "destination_city",
        "departure", "arrival", "car_reg", "total_seats", "price_per_seat"
    )
    list_filter = ("transport_type", "operator_name", "origin_city", "destination_city")
    search_fields = ("operator_name", "origin_city", "destination_city", "car_reg")
    date_hierarchy = "departure"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("hotel_id", "account_id", "rating", "staff_user", "parent", "eco_rating", "create_at")
    list_filter = ("rating", "eco_rating", "create_at")
    search_fields = ("hotel_id__name", "account_id__fname", "account_id__lname", "staff_user__username", "comment")
    autocomplete_fields = ("hotel_id", "account_id", "staff_user", "parent")
    readonly_fields = ("create_at",)

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room_type", "check_in", "check_out", "room_booked", "created_at")
    list_filter = ("check_in", "check_out", "created_at", "room_type__hotel")
    search_fields = ("user__email", "room_type__name", "room_type__hotel__name")
    autocomplete_fields = ("user", "room_type")
    readonly_fields = ("created_at",)

@admin.register(TripBooking)
class TripBookingAdmin(admin.ModelAdmin):
    list_display = ("user", "trip", "seats_booked", "created_at")
    list_filter = ("created_at", "trip__transport_type", "trip__origin_city", "trip__destination_city")
    search_fields = ("user__email", "trip__operator_name", "trip__origin_city", "trip__destination_city", "trip__car_reg")
    autocomplete_fields = ("user", "trip")
    readonly_fields = ("created_at",)

# -------- Optional: Admin branding --------
admin.site.site_header = "Booking Admin"
admin.site.site_title = "Booking Admin"
admin.site.index_title = "Administration"