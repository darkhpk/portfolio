from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password, make_password, identify_hasher
from .models import RoomBooking, TripBooking, User as CustomerUser, Review, Hotel, Room, TransportationTrip

def _looks_hashed(value: str) -> bool:
    """
    Return True if value looks like a Django password hash (e.g. 'pbkdf2_sha256$...').
    """
    try:
        identify_hasher(value)
        return True
    except Exception:
        return False

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class SearchForm(forms.Form):
    SEARCH_CHOICES = (
        ('hotel', 'Hotel'),
        ('transport', 'Transportation'),
    )
    search_type = forms.ChoiceField(choices=SEARCH_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    city_from = forms.CharField(required=False, label="From", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}))
    city_to = forms.CharField(required=False, label="To / City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}))
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    departure = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    persons = forms.IntegerField(required=False, min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1'}))
    
    def clean(self):
        cleaned_data = super().clean()
        search_type = cleaned_data.get('search_type')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        
        # Validate hotel search dates
        if search_type == 'hotel' and check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError('Check-out date must be after check-in date.')
            
            # Prevent past dates
            from datetime import date
            if check_in < date.today():
                raise forms.ValidationError('Check-in date cannot be in the past.')
        
        return cleaned_data

class RoomBookingForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        error_messages={'required': 'You must accept the terms and conditions to proceed.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Guest fields (optional)
    guest_name = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }),
        label='Your Name'
    )
    guest_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        }),
        label='Email Address'
    )
    guest_phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+40 XXX XXX XXX'
        }),
        label='Phone Number'
    )
    
    class Meta:
        model = RoomBooking
        fields = ("check_in", "check_out", "room_booked", "guest_name", "guest_email", "guest_phone")
        widgets = {
            "check_in": forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select check-in date'
            }),
            "check_out": forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select check-out date'
            }),
            "room_booked": forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of rooms'
            }),
        }
        labels = {
            'check_in': 'Check-in Date',
            'check_out': 'Check-out Date',
            'room_booked': 'Number of Rooms',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get('guest_name')
        guest_email = cleaned_data.get('guest_email')
        guest_phone = cleaned_data.get('guest_phone')
        
        # If any guest field is filled, all must be filled
        guest_fields = [guest_name, guest_email, guest_phone]
        if any(guest_fields):
            if not all(guest_fields):
                raise forms.ValidationError('Please fill in all guest information fields (name, email, and phone).')
        
        return cleaned_data

class TripBookingForm(forms.ModelForm):
    terms_accepted = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
        error_messages={'required': 'You must accept the terms and conditions to proceed.'},
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Guest fields (optional)
    guest_name = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        }),
        label='Your Name'
    )
    guest_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        }),
        label='Email Address'
    )
    guest_phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+40 XXX XXX XXX'
        }),
        label='Phone Number'
    )
    
    class Meta:
        model = TripBooking
        fields = ("seats_booked", "guest_name", "guest_email", "guest_phone")
        widgets = {
            "seats_booked": forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Number of seats'
            }),
        }
        labels = {
            'seats_booked': 'Number of Seats',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        guest_name = cleaned_data.get('guest_name')
        guest_email = cleaned_data.get('guest_email')
        guest_phone = cleaned_data.get('guest_phone')
        
        # If any guest field is filled, all must be filled
        guest_fields = [guest_name, guest_email, guest_phone]
        if any(guest_fields):
            if not all(guest_fields):
                raise forms.ValidationError('Please fill in all guest information fields (name, email, and phone).')
        
        return cleaned_data

class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}), label="Email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}), label="Password")

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        raw = cleaned.get("password")

        if not email or not raw:
            return cleaned

        try:
            user = CustomerUser.objects.get(email=email)
        except CustomerUser.DoesNotExist:
            raise ValidationError("No account found with this email.")

        stored = user.password or ""

        if _looks_hashed(stored):
            # Normal path: verify with hasher
            if not check_password(raw, stored):
                raise ValidationError("Incorrect password.")
        else:
            # Legacy plaintext stored: verify by equality, then upgrade to hashed
            if stored != raw:
                raise ValidationError("Incorrect password.")
            user.password = make_password(raw)
            user.save(update_fields=["password"])

        cleaned["user"] = user
        return cleaned
    
class CustomerSignupForm(forms.Form):
    USER_ROLE_CHOICES = (
        ('customer', 'Customer - Book hotels and transportation'),
        ('hotel_manager', 'Hotel Manager - Manage hotel listings'),
        ('transport_manager', 'Transport Manager - Manage transportation services'),
    )
    
    user_role = forms.ChoiceField(
        choices=USER_ROLE_CHOICES,
        label="Account Type",
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        initial='customer'
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"placeholder": "you@example.com", "class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "class": "form-control"})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••", "class": "form-control"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if CustomerUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("confirm_password")
        if p1 and p2 and p1 != p2:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned

    def save(self):
        data = self.cleaned_data
        return CustomerUser.objects.create(
            email=data["email"],
            password=make_password(data["password"]),
            user_role=data["user_role"],
        )
    
class HotelReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "eco_rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "eco_rating": forms.NumberInput(attrs={"min": 1, "max": 5, "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 4, "class": "form-control", "placeholder": "Write your review..."}),
        }

class AddHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'city', 'address', 'description', 'thumbnail_url', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hotel name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your hotel...'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'eco-friendly, family, business'}),
        }
        labels = {
            'thumbnail_url': 'Hotel Image URL',
            'tags': 'Tags (comma-separated)',
        }

class AddRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'max_persons', 'price_per_night', 'total_rooms']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Deluxe Suite, Standard Room, etc.'}),
            'max_persons': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '2'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '99.99'}),
            'total_rooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '10'}),
        }
        labels = {
            'max_persons': 'Maximum Persons per Room',
            'price_per_night': 'Price per Night (£)',
            'total_rooms': 'Total Available Rooms',
        }

class AddTransportationForm(forms.ModelForm):
    class Meta:
        model = TransportationTrip
        fields = ['transport_type', 'operator_name', 'origin_city', 'destination_city', 
                  'departure', 'arrival', 'car_reg', 'total_seats', 'price_per_seat', 'thumbnail_url']
        widgets = {
            'transport_type': forms.Select(attrs={'class': 'form-select'}),
            'operator_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company name'}),
            'origin_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Departure city'}),
            'destination_city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Arrival city'}),
            'departure': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'arrival': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'car_reg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle registration number'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '50'}),
            'price_per_seat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '29.99'}),
            'thumbnail_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/image.jpg'}),
        }
        labels = {
            'car_reg': 'Vehicle Registration',
            'price_per_seat': 'Price per Seat (£)',
            'thumbnail_url': 'Vehicle/Route Image URL',
        }