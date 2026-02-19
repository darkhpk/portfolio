from datetime import date
import random
import logging
from functools import wraps
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.db import models
from .forms import (
    SearchForm, RoomBookingForm, 
    TripBookingForm, SignUpForm, 
    EmailLoginForm, CustomerSignupForm,
    HotelReviewForm, AddHotelForm, AddRoomForm, AddTransportationForm
)
from .models import (
    Hotel, Room, 
    RoomBooking, TransportationTrip, 
    TripBooking, User as CustomerUser,
    Review, Account
)

logger = logging.getLogger(__name__)


def customer_login_required(view_func):
    """
    Decorator for views that require customer session authentication.
    Redirects to customer login page if not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "customer_id" not in request.session:
            form = EmailLoginForm()
            messages.info(request, "Please log in to continue.")
            return render(request, "booking/customer_login.html", {"form": form})
        
        # Validate customer exists
        try:
            customer = CustomerUser.objects.get(id=request.session.get("customer_id"))
            request.customer = customer  # Attach to request for convenience
        except CustomerUser.DoesNotExist:
            request.session.flush()
            form = EmailLoginForm()
            messages.error(request, "Your session has expired. Please log in again.")
            return render(request, "booking/customer_login.html", {"form": form})
        
        return view_func(request, *args, **kwargs)
    return wrapper


def toggle_darkmode(request):
    try:
        current = request.session.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"
        request.session["theme"] = new_theme
        logger.info(f'Theme: {request.session.get("theme")}')
    except Exception as e:
        logger.error(f"Problem at toggle of darkmode/lightmode >> {e}")
    return redirect(request.META.get("HTTP_REFERER", "home"))

def signup_view(request):
    try:
        if request.method == 'POST':
            try:
                form = SignUpForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Account created. You can now log in.')
                    return redirect('login')
                else:
                    messages.error(request, 'Please correct the errors below.')
            except Exception as e:
                logger.error(f'Problem at signing up in admin panel >> {e}')
                messages.error(request, 'An error occurred during signup.')
                form = SignUpForm(request.POST)
        else:
            form = SignUpForm()
        return render(request, 'booking/signup.html', {'form': form})
    except Exception as e:
        logger.error(f"Problems at signing up in admin panel >> {e}")
        messages.error(request, 'An unexpected error occurred.')
        return redirect('website:search')

def _can_manage_review(request, review: Review) -> bool:
    """
    Allow if:
      - Django admin/staff
      - Poster staff user (for replies created by staff)
      - Poster customer (session-based) whose Account matches review.account_id
    """
    try:
        # Admin/staff
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            logger.info(f'Admin {request.user.id} tries to manage reviews')
            return True

        # Staff poster
        if request.user.is_authenticated and review.staff_user_id and review.staff_user_id == request.user.id:
            logger.info(f'Admin {request.user.id} tries to manage reviews')
            return True

        # Customer poster via session
        customer_id = request.session.get("customer_id")
        if customer_id:
            try:
                customer = CustomerUser.objects.get(id=customer_id)
            except CustomerUser.DoesNotExist:
                customer = None
            logger.info(f'Customer {customer} tries to manage reviews')
            if customer:
                # If Account has FK to CustomerUser and no related_name, reverse is account_set
                account = customer.account_set.first()
                if account and review.account_id_id == account.id:
                    return True
    except Exception as e:
        logger.error(f"Problems at checking permission for reviews >> {e}")
    return False

def login_view(request):
    try:
        if request.method == 'POST':
            try:
                form = AuthenticationForm(request, data=request.POST)
                if form.is_valid():
                    username = form.cleaned_data.get('username')
                    password = form.cleaned_data.get('password')
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        request.session["admin_id"] = user.id
                        request.session["admin_username"] = user.username
                        request.session["admin_email"] = user.email
                        login(request, user)
                        logger.info(f"Admin [{user.id}]{user.username} has logged in!")
                        messages.success(request, f'Welcome back, {username}!')
                        return redirect('website:search')
                    else:
                        logger.warning(f"Someone entered wrong username or password >> {username}")
                        messages.error(request, 'Invalid username or password.')
                else:
                    messages.error(request, 'Invalid credentials.')
            except Exception as e:
                logger.error(f"Problems at checking login credentials >> {e}")
                messages.error(request, 'An error occurred during login.')
                form = AuthenticationForm(request, data=request.POST)
        else:
            form = AuthenticationForm()
        return render(request, 'booking/login.html', {'form': form})
    except Exception as e:
        logger.error(f"Problems at posting the login request >> {e}")
        messages.error(request, 'An unexpected error occurred.')
        return redirect('website:search')

def logout_view(request):
    try:
        if request.user.is_authenticated:
            logout(request)
        request.session.flush()
        messages.info(request, 'You have been logged out.')
        return redirect('login')
    except Exception as e:
        logger.error(f"Problems at logging out >> {e}")
        return redirect('website:search')

def customer_signup(request):
    if request.method == "POST":
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created! You can now log in.")
            return redirect("customer_login")
    else:
        form = CustomerSignupForm()
    return render(request, "booking/customer_signup.html", {"form": form})

def customer_login(request):
    if not request.session.get("customer_id"):
        if request.method == "POST":
            form = EmailLoginForm(request.POST)
            if form.is_valid():
                user = form.cleaned_data["user"]
                # Create session
                request.session["customer_id"] = user.id
                request.session["customer_email"] = user.email
                messages.success(request, f"Welcome, {user.email}!")
                return redirect("customer_dashboard")
        else:
            form = EmailLoginForm()
    else:
        email = request.session.get("customer_email")
        messages.success(request, f"Welcome, {email}!")
        return redirect("customer_dashboard")
    return render(request, "booking/customer_login.html", {"form": form})

def customer_logout(request):
    request.session.flush()
    form = EmailLoginForm()
    messages.info(request, "You have been logged out.")
    return render(request, "booking/customer_login.html", {"form": form})

def customer_dashboard(request):
    if request.session.get("admin_id") is not None:
        admin_user = {
            "id": request.session.get("admin_id"),
            "username": request.session.get("admin_username"),
            "email": request.session.get("admin_email")
        }
        return render(request, "booking/customer_dashboard.html", {"admin": admin_user}) 
    if "customer_id" not in request.session:
        form = EmailLoginForm()
        messages.info(request, "Please log in to view your dashboard.")
        return render(request, "booking/customer_login.html", {"form": form})
    
    try:
        user = CustomerUser.objects.get(id=request.session.get("customer_id"))
    except CustomerUser.DoesNotExist:
        request.session.flush()
        form = EmailLoginForm()
        messages.error(request, "Your session has expired. Please log in again.")
        return render(request, "booking/customer_login.html", {"form": form})
    
    # Redirect managers to manager dashboard
    if user.user_role in ['hotel_manager', 'transport_manager']:
        return redirect(reverse('manager_dashboard'))
    
    account = user.account_set.first()
    room_booking = RoomBooking.objects.filter(user=user)
    rooms = []
    trips = []
    if room_booking:
        for e in room_booking:
            rooms.append({
                "booking_nr": e.booking_nr,
                "date": e.created_at,
                "name": e.room_type.hotel.name,
                "location": e.room_type.hotel.address,
                "checkin": e.check_in,
                "checkout": e.check_out,
                "price": (e.room_type.price_per_night * e.room_booked)
            })
    trip_booking = TripBooking.objects.filter(user=user)
    if trip_booking:
        for e in trip_booking:
            trips.append({
                "booking_nr": e.booking_nr,
                "date": e.created_at,
                "trip": e.trip,
                "seats": e.seats_booked,
                "price": e.trip.price_per_seat
            })
    return render(request, "booking/customer_dashboard.html", {"user": user, "account": account, "room_booking": rooms, "trip_booking": trips})

def search_view(request):
    if "customer_id" not in request.session:
        form = SearchForm(request.GET or None)
        return render(request, 'booking/search.html', {'form': form})
    else:
        user = CustomerUser.objects.get(id=request.session.get("customer_id"))
        form = SearchForm(request.GET or None)
        return render(request, 'booking/search.html', {'form': form, 'user': user})

def results_view(request):
    form = SearchForm(request.GET)
    if "customer_id" in request.session:
        user = CustomerUser.objects.get(id=request.session.get("customer_id"))
        context = {'form': form, 'hotels': [], 'trips': [], 'user': user}
    else:
        context = {'form': form, 'hotels': [], 'trips': []}
        
    if not form.is_valid():
        messages.error(request, 'Invalid search input')
        return render(request, 'booking/results.html', context)

    search_type = form.cleaned_data['search_type']
    persons = form.cleaned_data.get('persons') or 1
    sort_by = request.GET.get('sort_by', 'name')  # name, price_low, price_high, rating

    if search_type == 'hotel':
        city = form.cleaned_data.get('city_to') or ''
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')
        
        # Base hotel query with prefetch for efficiency
        hotels = Hotel.objects.filter(city__icontains=city).prefetch_related('rooms', 'reviews')
        
        # Filter hotels that have rooms available for the person count
        hotel_results = []
        for h in hotels:
            suitable_rooms = [r for r in h.rooms.all() if r.max_persons >= persons]
            if not suitable_rooms:
                continue
            
            # Find cheapest suitable room
            cheapest_room = min(suitable_rooms, key=lambda x: x.price_per_night)
            
            # Check availability if dates provided
            available = True
            if check_in and check_out and check_in < check_out:
                available_count = _rooms_available(cheapest_room, check_in, check_out)
                available = available_count > 0
            
            if available or not (check_in and check_out):
                # Calculate average rating
                avg_rating = h.reviews.filter(parent__isnull=True).aggregate(
                    avg=models.Avg('rating')
                )['avg'] or 0
                
                hotel_results.append({
                    'obj': h,
                    'cheapest_room': cheapest_room,
                    'price': float(cheapest_room.price_per_night),
                    'avg_rating': round(avg_rating, 1)
                })
        
        # Sort results
        if sort_by == 'price_low':
            hotel_results.sort(key=lambda x: x['price'])
        elif sort_by == 'price_high':
            hotel_results.sort(key=lambda x: x['price'], reverse=True)
        elif sort_by == 'rating':
            hotel_results.sort(key=lambda x: x['avg_rating'], reverse=True)
        else:  # name
            hotel_results.sort(key=lambda x: x['obj'].name)
        
        context['hotels'] = hotel_results
        context['check_in'] = check_in
        context['check_out'] = check_out
        context['persons'] = persons
        
    else:
        city_from = form.cleaned_data.get('city_from') or ''
        city_to = form.cleaned_data.get('city_to') or ''
        departure = form.cleaned_data.get('departure')
        
        # Base transportation query
        trips = TransportationTrip.objects.filter(
            origin_city__icontains=city_from,
            destination_city__icontains=city_to,
        )
        
        if departure:
            trips = trips.filter(departure__date=departure.date())
        
        # Filter trips with available seats and add booking count
        trip_results = []
        for trip in trips:
            booked_seats = TripBooking.objects.filter(trip=trip).aggregate(
                total=Sum('seats_booked')
            )['total'] or 0
            available_seats = trip.total_seats - booked_seats
            
            if available_seats >= persons:
                trip_results.append({
                    'obj': trip,
                    'available_seats': available_seats,
                    'price': float(trip.price_per_seat)
                })
        
        # Sort trips
        if sort_by == 'price_low':
            trip_results.sort(key=lambda x: x['price'])
        elif sort_by == 'price_high':
            trip_results.sort(key=lambda x: x['price'], reverse=True)
        elif sort_by == 'time':
            trip_results.sort(key=lambda x: x['obj'].departure)
        else:
            trip_results.sort(key=lambda x: x['obj'].departure)
        
        context['trips'] = trip_results
        context['departure'] = departure
    
    context['sort_by'] = sort_by
    context['search_type'] = search_type
    return render(request, 'booking/results.html', context)

def _rooms_available(room_type: Room, start: date, end: date) -> int:
    if end <= start:
        return 0
    overlapping = RoomBooking.objects.filter(
        room_type=room_type,
        check_in__lt=end,
        check_out__gt=start,
    ).aggregate(total=Sum('room_booked'))['total'] or 0
    return max(room_type.total_rooms - overlapping, 0)

def hotel_detail(request, pk: int):
    logged_in = False
    if "customer_id" in request.session:
        logged_in = True
        user = CustomerUser.objects.get(id=request.session.get("customer_id"))
    hotel = get_object_or_404(Hotel, pk=pk)

    # --- read dates from querystring ---
    q_check_in = request.GET.get("check_in") or ""
    q_check_out = request.GET.get("check_out") or ""
    check_in = parse_date(q_check_in)
    check_out = parse_date(q_check_out)

    # sanitize invalid ranges
    if check_in and check_out and check_in >= check_out:
        messages.warning(request, "Check-out must be after check-in.")
        check_in, check_out = None, None

    # --- build rooms_info only when dates are present ---
    rooms_info = []
    if check_in and check_out:
        for r in hotel.rooms.all():
            # If you already have a helper, call it here:
            # available = _rooms_available(r, check_in, check_out)
            # Otherwise, a simple overlap check (adjust model/field names if needed):
            booked_overlap = RoomBooking.objects.filter(
                room_type=r,
                check_in__lt=check_out,
                check_out__gt=check_in,
            ).exists()
            available = 0 if booked_overlap else 1  # replace with your capacity logic
            rooms_info.append({"room": r, "available": available})
    else:
        rooms_info = None  # triggers "Select dates" UI

    avg_rating = (
        hotel.reviews.filter(parent__isnull=True)
            .aggregate(avg_rating=models.Avg("rating"))  # <- explicit alias
            .get("avg_rating")                  # <- safe read
    ) or 0
    eco_avg_rating = (
        hotel.reviews.filter(parent__isnull=True)
            .aggregate(eco_avg_rating=models.Avg("eco_rating"))  # <- explicit alias
            .get("eco_avg_rating")
    ) or 0
    # your existing reviews logic here...
    reviews = hotel.reviews.filter(parent__isnull=True).select_related("account_id", "staff_user")
    
    if logged_in:
        context = {
            "hotel": hotel,
            "reviews": reviews,
            "eco_avg_rating": round(eco_avg_rating, 1),
            "avg_rating": round(avg_rating, 1),
            "rooms_info": rooms_info,
            "check_in": check_in,
            "check_out": check_out,
            "q_check_in": q_check_in,   # keep originals for form fields
            "q_check_out": q_check_out,
            "user": user,
        }
    else:
        context = {
            "hotel": hotel,
            "reviews": reviews,
            "eco_avg_rating": round(eco_avg_rating, 1),
            "avg_rating": round(avg_rating, 1),
            "rooms_info": rooms_info,
            "check_in": check_in,
            "check_out": check_out,
            "q_check_in": q_check_in,   # keep originals for form fields
            "q_check_out": q_check_out,
        }
    return render(request, "booking/hotel_detail.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def reply_to_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    hotel = review.hotel_id

    if request.method == "POST":
        text = request.POST.get("comment", "").strip()
        if not text:
            messages.error(request, "Reply cannot be empty.")
            return redirect("website:hotel_detail", pk=hotel.id)

        Review.objects.create(
            hotel_id=hotel,
            parent=review,
            staff_user=request.user,
            rating=review.rating,
            eco_rating=review.eco_rating,  # inherit rating or set to 0 if you prefer
            comment=text,
        )
        messages.success(request, "Reply posted.")
        return redirect("website:hotel_detail", pk=hotel.id)

    # simple fallback form
    return render(request, "booking/reply_review.html", {
        "review": review,
        "hotel": hotel,
    })

def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Check if customer is logged in via session
    if "customer_id" not in request.session:
        form = EmailLoginForm()
        messages.info(request, "Please log in to write a review.")
        return render(request, "booking/customer_login.html", {"form": form})

    # Get customer's account
    try:
        customer = CustomerUser.objects.get(id=request.session.get("customer_id"))
        account = customer.account_set.first()
    except CustomerUser.DoesNotExist:
        request.session.flush()
        form = EmailLoginForm()
        messages.error(request, "Your session has expired. Please log in again.")
        return render(request, "booking/customer_login.html", {"form": form})
    
    if request.method == "POST":
        comment = request.POST.get("comment", "").strip()
        rate = request.POST.get("rate")
        eco_rate = request.POST.get("eco_rate")

        # Validate comment
        if not comment:
            messages.error(request, "Please write something before submitting your review.")
            return redirect("website:hotel_detail", pk=hotel.id)

        # Create Review instance
        Review.objects.create(
            hotel_id=hotel,
            account_id=account,
            rating=rate or 0,
            eco_rating=eco_rate or 0,
            comment=comment,
        )

        messages.success(request, "Your review has been posted successfully!")
        return redirect("website:hotel_detail", pk=hotel.id)

    # Fallback: prevent GET access
    messages.warning(request, "Invalid access method.")
    return redirect("website:hotel_detail", pk=hotel.id)

@require_POST
def edit_review(request, review_id: int):
    review = get_object_or_404(Review, pk=review_id)
    hotel = review.hotel_id  # FK -> Hotel instance

    if not _can_manage_review(request, review):
        messages.error(request, "You don't have permission to edit this comment.")
        return redirect("website:hotel_detail", pk=hotel.id)

    new_comment = (request.POST.get("comment") or "").strip()
    if not new_comment:
        messages.error(request, "Comment cannot be empty.")
        return redirect("website:hotel_detail", pk=hotel.id)

    review.comment = new_comment
    review.save(update_fields=["comment"])
    messages.success(request, "Comment updated successfully.")
    return redirect("website:hotel_detail", pk=hotel.id)

@require_POST
def delete_review(request, review_id: int):
    review = get_object_or_404(Review, pk=review_id)
    hotel = review.hotel_id  # keep before delete

    if not _can_manage_review(request, review):
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect("website:hotel_detail", pk=hotel.id)

    review.delete()
    messages.success(request, "Comment deleted.")
    return redirect("website:hotel_detail", pk=hotel.id)

def _seats_available(trip: TransportationTrip) -> int:
    booked = TripBooking.objects.filter(trip=trip).aggregate(total=Sum('seats_booked'))['total'] or 0
    return max(trip.total_seats - booked, 0)

def transportation_detail(request, pk: int):
    trip = get_object_or_404(TransportationTrip, pk=pk)
    available = _seats_available(trip)
    return render(request, 'booking/transportation_detail.html', {'trip': trip, 'available': available})

def book_room(request, room_type_id: int):
    room_type = get_object_or_404(Room, pk=room_type_id)
    
    # Check if user is logged in
    is_logged_in = "customer_id" in request.session
    customer = None
    
    if is_logged_in:
        try:
            customer = CustomerUser.objects.get(id=request.session.get("customer_id"))
        except CustomerUser.DoesNotExist:
            request.session.flush()
            is_logged_in = False
    
    if request.method == 'POST':
        form = RoomBookingForm(request.POST)
        if form.is_valid():
            booking_number = random.randint(10000, 99999)
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            rooms_booked = form.cleaned_data['room_booked']
            
            # Check if this is a guest booking
            guest_name = form.cleaned_data.get('guest_name')
            guest_email = form.cleaned_data.get('guest_email')
            guest_phone = form.cleaned_data.get('guest_phone')
            is_guest_booking = bool(guest_name and guest_email and guest_phone)
            
            # Validate guest booking if user not logged in
            if not is_logged_in and not is_guest_booking:
                messages.error(request, 'Please provide your contact information or log in to continue.')
                return render(request, 'booking/booking_room.html', {
                    'room_type': room_type,
                    'form': form,
                    'is_logged_in': is_logged_in
                })
            
            available = _rooms_available(room_type, check_in, check_out)
            if rooms_booked > available:
                messages.error(request, f'Only {available} room(s) available for that range')
            else:
                RoomBooking.objects.create(
                    user=customer if is_logged_in else None,
                    room_type=room_type,
                    check_in=check_in,
                    check_out=check_out,
                    room_booked=rooms_booked,
                    booking_nr=booking_number,
                    is_guest=is_guest_booking,
                    guest_name=guest_name if is_guest_booking else None,
                    guest_email=guest_email if is_guest_booking else None,
                    guest_phone=guest_phone if is_guest_booking else None
                )
                
                if is_guest_booking:
                    messages.success(request, f'Room booked successfully! Booking number: {booking_number}. A confirmation has been sent to {guest_email}.')
                else:
                    messages.success(request, 'Room booked successfully!')
                
                return redirect('website:hotel_detail', pk=room_type.hotel_id)
    else:
        form = RoomBookingForm(initial={
            'check_in': request.GET.get('check_in'),
            'check_out': request.GET.get('check_out'),
        })
    
    return render(request, 'booking/booking_room.html', {
        'room_type': room_type,
        'form': form,
        'is_logged_in': is_logged_in
    })

def book_trip(request, trip_id: int):
    trip = get_object_or_404(TransportationTrip, pk=trip_id)
    
    # Check if user is logged in
    is_logged_in = "customer_id" in request.session
    customer = None
    
    if is_logged_in:
        try:
            customer = CustomerUser.objects.get(id=request.session.get("customer_id"))
        except CustomerUser.DoesNotExist:
            request.session.flush()
            is_logged_in = False
    
    available = _seats_available(trip)
    
    if request.method == "POST":
        form = TripBookingForm(request.POST)
        booking_number = random.randint(10000, 99999)
        if form.is_valid():
            seats = form.cleaned_data['seats_booked']
            
            # Check if this is a guest booking
            guest_name = form.cleaned_data.get('guest_name')
            guest_email = form.cleaned_data.get('guest_email')
            guest_phone = form.cleaned_data.get('guest_phone')
            is_guest_booking = bool(guest_name and guest_email and guest_phone)
            
            # Validate guest booking if user not logged in
            if not is_logged_in and not is_guest_booking:
                messages.error(request, 'Please provide your contact information or log in to continue.')
                return render(request, 'booking/booking_trip.html', {
                    'trip': trip,
                    'form': form,
                    'available': available,
                    'is_logged_in': is_logged_in
                })
            
            if seats > available:
                messages.error(request, f'Only {available} seat(s) available.')
            else:
                TripBooking.objects.create(
                    user=customer if is_logged_in else None,
                    trip=trip,
                    seats_booked=seats,
                    booking_nr=booking_number,
                    is_guest=is_guest_booking,
                    guest_name=guest_name if is_guest_booking else None,
                    guest_email=guest_email if is_guest_booking else None,
                    guest_phone=guest_phone if is_guest_booking else None
                )
                
                if is_guest_booking:
                    messages.success(request, f'Seat(s) booked successfully! Booking number: {booking_number}. A confirmation has been sent to {guest_email}.')
                else:
                    messages.success(request, 'Seat(s) booked successfully!')
                
                return redirect('website:transportation_detail', pk=trip.id)
    else:
        form = TripBookingForm()
    
    return render(request, 'booking/booking_trip.html', {
        'trip': trip,
        'form': form,
        'available': available,
        'is_logged_in': is_logged_in
    })  


# Manager Dashboard and Management Views

def manager_login_required(view_func):
    """
    Decorator for views that require manager session authentication.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "customer_id" not in request.session:
            form = EmailLoginForm()
            messages.info(request, "Please log in to continue.")
            return render(request, "booking/customer_login.html", {"form": form})
        
        try:
            manager = CustomerUser.objects.get(id=request.session.get("customer_id"))
            if manager.user_role == 'customer':
                messages.error(request, "This area is for managers only.")
                return redirect("website:search")
            request.manager = manager
        except CustomerUser.DoesNotExist:
            request.session.flush()
            form = EmailLoginForm()
            messages.error(request, "Your session has expired. Please log in again.")
            return render(request, "booking/customer_login.html", {"form": form})
        
        return view_func(request, *args, **kwargs)
    return wrapper

@manager_login_required
def manager_dashboard(request):
    """Dashboard for hotel and transport managers"""
    manager = request.manager
    
    if manager.is_hotel_manager():
        hotels = Hotel.objects.filter(manager_user=manager)
        context = {
            'manager': manager,
            'hotels': hotels,
            'is_hotel_manager': True,
        }
    elif manager.is_transport_manager():
        trips = TransportationTrip.objects.filter(manager_user=manager)
        context = {
            'manager': manager,
            'trips': trips,
            'is_transport_manager': True,
        }
    else:
        context = {'manager': manager}
    
    return render(request, 'manager/dashboard.html', context)

@manager_login_required
def add_hotel(request):
    """Add new hotel (hotel managers only)"""
    manager = request.manager
    
    if not manager.is_hotel_manager():
        messages.error(request, "Only hotel managers can add hotels.")
        return redirect("manager_dashboard")
    
    if request.method == "POST":
        form = AddHotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.manager_user = manager
            hotel.save()
            messages.success(request, f"Hotel '{hotel.name}' added successfully!")
            return redirect("manager_dashboard")
    else:
        form = AddHotelForm()
    
    return render(request, 'manager/add_hotel.html', {'form': form, 'manager': manager})

@manager_login_required
def add_room(request, hotel_id):
    """Add room to existing hotel"""
    manager = request.manager
    hotel = get_object_or_404(Hotel, pk=hotel_id, manager_user=manager)
    
    if request.method == "POST":
        form = AddRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            messages.success(request, f"Room type '{room.name}' added to {hotel.name}!")
            return redirect("manager_dashboard")
    else:
        form = AddRoomForm()
    
    return render(request, 'manager/add_room.html', {'form': form, 'hotel': hotel, 'manager': manager})

@manager_login_required
def add_transportation(request):
    """Add new transportation trip (transport managers only)"""
    manager = request.manager
    
    if not manager.is_transport_manager():
        messages.error(request, "Only transport managers can add transportation.")
        return redirect("manager_dashboard")
    
    if request.method == "POST":
        form = AddTransportationForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.manager_user = manager
            trip.save()
            messages.success(request, f"Transportation from {trip.origin_city} to {trip.destination_city} added successfully!")
            return redirect("manager_dashboard")
    else:
        form = AddTransportationForm()
    
    return render(request, 'manager/add_transportation.html', {'form': form, 'manager': manager})

@manager_login_required
def edit_hotel(request, hotel_id):
    """Edit existing hotel"""
    manager = request.manager
    hotel = get_object_or_404(Hotel, pk=hotel_id, manager_user=manager)
    
    if request.method == "POST":
        form = AddHotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, f"Hotel '{hotel.name}' updated successfully!")
            return redirect("manager_dashboard")
    else:
        form = AddHotelForm(instance=hotel)
    
    return render(request, 'manager/edit_hotel.html', {'form': form, 'hotel': hotel, 'manager': manager})

@manager_login_required
def edit_transportation(request, trip_id):
    """Edit existing transportation trip"""
    manager = request.manager
    trip = get_object_or_404(TransportationTrip, pk=trip_id, manager_user=manager)
    
    if request.method == "POST":
        form = AddTransportationForm(request.POST, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, f"Transportation updated successfully!")
            return redirect("manager_dashboard")
    else:
        form = AddTransportationForm(instance=trip)
    
    return render(request, 'manager/edit_transportation.html', {'form': form, 'trip': trip, 'manager': manager})

@manager_login_required
def delete_hotel(request, hotel_id):
    """Delete hotel"""
    manager = request.manager
    hotel = get_object_or_404(Hotel, pk=hotel_id, manager_user=manager)
    
    if request.method == "POST":
        hotel_name = hotel.name
        hotel.delete()
        messages.success(request, f"Hotel '{hotel_name}' deleted successfully!")
        return redirect("manager_dashboard")
    
    return render(request, 'manager/confirm_delete.html', {'object': hotel, 'type': 'hotel', 'manager': manager})

@manager_login_required
def delete_transportation(request, trip_id):
    """Delete transportation trip"""
    manager = request.manager
    trip = get_object_or_404(TransportationTrip, pk=trip_id, manager_user=manager)
    
    if request.method == "POST":
        trip_info = f"{trip.origin_city} to {trip.destination_city}"
        trip.delete()
        messages.success(request, f"Transportation '{trip_info}' deleted successfully!")
        return redirect("manager_dashboard")
    
    return render(request, 'manager/confirm_delete.html', {'object': trip, 'type': 'transportation', 'manager': manager})


# Custom error handlers
def handler404(request, exception):
    """Custom 404 page"""
    return render(request, '404.html', status=404)


def handler500(request):
    """Custom 500 page"""
    return render(request, '500.html', status=500)


def handler403(request, exception):
    """Custom 403 page"""
    return render(request, '403.html', status=403)  
