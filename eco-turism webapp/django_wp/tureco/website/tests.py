"""
Automated Test Suite for Role-Based Manager System
Run with: python manage.py test website.tests
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import User, Hotel, Room, TransportationTrip, RoomBooking, TripBooking
from datetime import datetime, timedelta


class UserRegistrationTests(TestCase):
    """Test user registration with different roles"""
    
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('customer_signup')
    
    def test_register_as_customer(self):
        """TC1.1: Register as Customer"""
        response = self.client.post(self.signup_url, {
            'user_role': 'customer',
            'email': 'customer@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after success
        user = User.objects.get(email='customer@test.com')
        self.assertEqual(user.user_role, 'customer')
    
    def test_register_as_hotel_manager(self):
        """TC1.2: Register as Hotel Manager"""
        response = self.client.post(self.signup_url, {
            'user_role': 'hotel_manager',
            'email': 'hotelmanager@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='hotelmanager@test.com')
        self.assertEqual(user.user_role, 'hotel_manager')
        self.assertTrue(user.is_hotel_manager())
    
    def test_register_as_transport_manager(self):
        """TC1.3: Register as Transport Manager"""
        response = self.client.post(self.signup_url, {
            'user_role': 'transport_manager',
            'email': 'transportmanager@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(email='transportmanager@test.com')
        self.assertEqual(user.user_role, 'transport_manager')
        self.assertTrue(user.is_transport_manager())
    
    def test_duplicate_email_registration(self):
        """TC1.4: Duplicate Email Registration"""
        User.objects.create(
            email='existing@test.com',
            password=make_password('testpass123'),
            user_role='customer'
        )
        
        response = self.client.post(self.signup_url, {
            'user_role': 'customer',
            'email': 'existing@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 200)  # Form redisplayed with errors
        self.assertFormError(response, 'form', 'email', 'Email already registered.')
    
    def test_password_mismatch(self):
        """TC1.5: Password Mismatch"""
        response = self.client.post(self.signup_url, {
            'user_role': 'customer',
            'email': 'newuser@test.com',
            'password': 'testpass123',
            'confirm_password': 'different123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'confirm_password', 'Passwords do not match.')


class UserLoginRoutingTests(TestCase):
    """Test login and dashboard routing for different user roles"""
    
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('customer_login')
        
        # Create test users
        self.customer = User.objects.create(
            email='customer@test.com',
            password=make_password('testpass123'),
            user_role='customer'
        )
        
        self.hotel_manager = User.objects.create(
            email='hotelmanager@test.com',
            password=make_password('testpass123'),
            user_role='hotel_manager'
        )
        
        self.transport_manager = User.objects.create(
            email='transportmanager@test.com',
            password=make_password('testpass123'),
            user_role='transport_manager'
        )
    
    def test_customer_login_routing(self):
        """TC2.1: Customer Login"""
        response = self.client.post(self.login_url, {
            'email': 'customer@test.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_dashboard'))
    
    def test_hotel_manager_login_routing(self):
        """TC2.2: Hotel Manager Login"""
        response = self.client.post(self.login_url, {
            'email': 'hotelmanager@test.com',
            'password': 'testpass123'
        })
        
        # Should redirect to customer_dashboard which then redirects to manager_dashboard
        self.assertEqual(response.status_code, 302)
    
    def test_transport_manager_login_routing(self):
        """TC2.3: Transport Manager Login"""
        response = self.client.post(self.login_url, {
            'email': 'transportmanager@test.com',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, 302)


class HotelManagementTests(TestCase):
    """Test hotel manager features"""
    
    def setUp(self):
        self.client = Client()
        
        # Create hotel manager
        self.manager = User.objects.create(
            email='hotelmanager@test.com',
            password=make_password('testpass123'),
            user_role='hotel_manager'
        )
        
        # Create another manager for security tests
        self.other_manager = User.objects.create(
            email='othermanager@test.com',
            password=make_password('testpass123'),
            user_role='hotel_manager'
        )
        
        # Login as hotel manager
        self.client.post(reverse('customer_login'), {
            'email': 'hotelmanager@test.com',
            'password': 'testpass123'
        })
    
    def test_view_manager_dashboard(self):
        """TC3.1: View Manager Dashboard"""
        response = self.client.get(reverse('website:manager_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manager Dashboard')
        self.assertContains(response, 'My Hotels')
    
    def test_add_new_hotel(self):
        """TC3.2: Add New Hotel"""
        response = self.client.post(reverse('website:add_hotel'), {
            'name': 'Grand Hotel Test',
            'city': 'Bucharest',
            'address': 'Test Street 123',
            'description': 'Test description',
            'thumbnail_url': 'https://example.com/hotel.jpg',
            'tags': 'eco-friendly, luxury'
        })
        
        self.assertEqual(response.status_code, 302)
        hotel = Hotel.objects.get(name='Grand Hotel Test')
        self.assertEqual(hotel.manager_user, self.manager)
        self.assertEqual(hotel.city, 'Bucharest')
    
    def test_add_room_to_hotel(self):
        """TC3.3: Add Room to Hotel"""
        hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Bucharest',
            address='Test Address',
            manager_user=self.manager
        )
        
        response = self.client.post(reverse('website:add_room', args=[hotel.id]), {
            'name': 'Deluxe Suite',
            'max_persons': 2,
            'price_per_night': 150.00,
            'total_rooms': 10
        })
        
        self.assertEqual(response.status_code, 302)
        room = Room.objects.get(name='Deluxe Suite')
        self.assertEqual(room.hotel, hotel)
        self.assertEqual(room.max_persons, 2)
    
    def test_edit_hotel(self):
        """TC3.4: Edit Hotel"""
        hotel = Hotel.objects.create(
            name='Original Hotel Name',
            city='Bucharest',
            address='Test Address',
            manager_user=self.manager
        )
        
        response = self.client.post(reverse('website:edit_hotel', args=[hotel.id]), {
            'name': 'Updated Hotel Name',
            'city': 'Bucharest',
            'address': 'Test Address',
            'description': 'Updated description',
            'thumbnail_url': '',
            'tags': ''
        })
        
        self.assertEqual(response.status_code, 302)
        hotel.refresh_from_db()
        self.assertEqual(hotel.name, 'Updated Hotel Name')
    
    def test_delete_hotel(self):
        """TC3.5: Delete Hotel"""
        hotel = Hotel.objects.create(
            name='Hotel to Delete',
            city='Bucharest',
            address='Test Address',
            manager_user=self.manager
        )
        hotel_id = hotel.id
        
        response = self.client.post(reverse('website:delete_hotel', args=[hotel.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Hotel.objects.filter(id=hotel_id).exists())
    
    def test_security_edit_other_manager_hotel(self):
        """TC3.6: Security - Cannot Edit Other Manager's Hotel"""
        other_hotel = Hotel.objects.create(
            name='Other Manager Hotel',
            city='Bucharest',
            address='Test Address',
            manager_user=self.other_manager
        )
        
        response = self.client.get(reverse('website:edit_hotel', args=[other_hotel.id]))
        
        self.assertEqual(response.status_code, 404)  # get_object_or_404 returns 404
    
    def test_security_customer_access_manager_pages(self):
        """TC3.7: Security - Customer Cannot Access Manager Pages"""
        # Logout and login as customer
        self.client.get(reverse('customer_logout'))
        
        customer = User.objects.create(
            email='customer@test.com',
            password=make_password('testpass123'),
            user_role='customer'
        )
        
        self.client.post(reverse('customer_login'), {
            'email': 'customer@test.com',
            'password': 'testpass123'
        })
        
        response = self.client.get(reverse('website:manager_dashboard'))
        
        # Should redirect with error message
        self.assertEqual(response.status_code, 302)


class TransportManagementTests(TestCase):
    """Test transport manager features"""
    
    def setUp(self):
        self.client = Client()
        
        self.manager = User.objects.create(
            email='transportmanager@test.com',
            password=make_password('testpass123'),
            user_role='transport_manager'
        )
        
        self.other_manager = User.objects.create(
            email='othertransport@test.com',
            password=make_password('testpass123'),
            user_role='transport_manager'
        )
        
        self.client.post(reverse('customer_login'), {
            'email': 'transportmanager@test.com',
            'password': 'testpass123'
        })
    
    def test_view_transport_dashboard(self):
        """TC4.1: View Transport Manager Dashboard"""
        response = self.client.get(reverse('website:manager_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Transportation Services')
    
    def test_add_new_transportation(self):
        """TC4.2: Add New Transportation"""
        departure = datetime.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=8)
        
        response = self.client.post(reverse('website:add_transportation'), {
            'transport_type': 'bus',
            'operator_name': 'Express Transport',
            'origin_city': 'Bucharest',
            'destination_city': 'Cluj-Napoca',
            'departure': departure.strftime('%Y-%m-%dT%H:%M'),
            'arrival': arrival.strftime('%Y-%m-%dT%H:%M'),
            'car_reg': 'B-123-ABC',
            'total_seats': 50,
            'price_per_seat': 75.00,
            'thumbnail_url': ''
        })
        
        self.assertEqual(response.status_code, 302)
        trip = TransportationTrip.objects.get(car_reg='B-123-ABC')
        self.assertEqual(trip.manager_user, self.manager)
        self.assertEqual(trip.origin_city, 'Bucharest')
    
    def test_edit_transportation(self):
        """TC4.3: Edit Transportation"""
        departure = datetime.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=8)
        
        trip = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='Test Transport',
            origin_city='Bucharest',
            destination_city='Cluj-Napoca',
            departure=departure,
            arrival=arrival,
            car_reg='B-TEST-123',
            total_seats=50,
            price_per_seat=75.00,
            manager_user=self.manager
        )
        
        response = self.client.post(reverse('website:edit_transportation', args=[trip.id]), {
            'transport_type': 'bus',
            'operator_name': 'Test Transport',
            'origin_city': 'Bucharest',
            'destination_city': 'Cluj-Napoca',
            'departure': departure.strftime('%Y-%m-%dT%H:%M'),
            'arrival': arrival.strftime('%Y-%m-%dT%H:%M'),
            'car_reg': 'B-TEST-123',
            'total_seats': 50,
            'price_per_seat': 80.00,  # Changed price
            'thumbnail_url': ''
        })
        
        self.assertEqual(response.status_code, 302)
        trip.refresh_from_db()
        self.assertEqual(float(trip.price_per_seat), 80.00)
    
    def test_delete_transportation(self):
        """TC4.4: Delete Transportation"""
        departure = datetime.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=8)
        
        trip = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='Test Transport',
            origin_city='Bucharest',
            destination_city='Cluj-Napoca',
            departure=departure,
            arrival=arrival,
            car_reg='B-DELETE-123',
            total_seats=50,
            price_per_seat=75.00,
            manager_user=self.manager
        )
        trip_id = trip.id
        
        response = self.client.post(reverse('website:delete_transportation', args=[trip.id]))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TransportationTrip.objects.filter(id=trip_id).exists())
    
    def test_security_edit_other_manager_trip(self):
        """TC4.5: Security - Cannot Edit Other Manager's Trip"""
        departure = datetime.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=8)
        
        other_trip = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='Other Transport',
            origin_city='Bucharest',
            destination_city='Cluj-Napoca',
            departure=departure,
            arrival=arrival,
            car_reg='B-OTHER-123',
            total_seats=50,
            price_per_seat=75.00,
            manager_user=self.other_manager
        )
        
        response = self.client.get(reverse('website:edit_transportation', args=[other_trip.id]))
        
        self.assertEqual(response.status_code, 404)


class CustomerIntegrationTests(TestCase):
    """Test customer booking integration with manager content"""
    
    def setUp(self):
        self.client = Client()
        
        # Create managers
        self.hotel_manager = User.objects.create(
            email='hotelmanager@test.com',
            password=make_password('testpass123'),
            user_role='hotel_manager'
        )
        
        self.transport_manager = User.objects.create(
            email='transportmanager@test.com',
            password=make_password('testpass123'),
            user_role='transport_manager'
        )
        
        # Create customer
        self.customer = User.objects.create(
            email='customer@test.com',
            password=make_password('testpass123'),
            user_role='customer'
        )
        
        # Create hotel with room
        self.hotel = Hotel.objects.create(
            name='Manager Hotel',
            city='Bucharest',
            address='Test Address',
            manager_user=self.hotel_manager
        )
        
        self.room = Room.objects.create(
            hotel=self.hotel,
            name='Standard Room',
            max_persons=2,
            price_per_night=100.00,
            total_rooms=10
        )
        
        # Create transportation
        departure = datetime.now() + timedelta(days=5)
        arrival = departure + timedelta(hours=8)
        
        self.trip = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='Manager Transport',
            origin_city='Bucharest',
            destination_city='Cluj-Napoca',
            departure=departure,
            arrival=arrival,
            car_reg='B-MGR-123',
            total_seats=50,
            price_per_seat=75.00,
            manager_user=self.transport_manager
        )
        
        # Login as customer
        self.client.post(reverse('customer_login'), {
            'email': 'customer@test.com',
            'password': 'testpass123'
        })
    
    def test_customer_views_manager_hotel(self):
        """TC5.1: Customer Can View Manager-Added Hotel"""
        response = self.client.get(reverse('website:hotel_detail', args=[self.hotel.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manager Hotel')
    
    def test_customer_views_manager_transportation(self):
        """TC5.2: Customer Can View Manager-Added Transportation"""
        response = self.client.get(reverse('website:transportation_detail', args=[self.trip.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Manager Transport')


class EdgeCaseTests(TestCase):
    """Test edge cases and error handling"""
    
    def setUp(self):
        self.client = Client()
    
    def test_unauthenticated_access_manager_dashboard(self):
        """TC6.1: Unauthenticated Access to Manager Pages"""
        response = self.client.get(reverse('website:manager_dashboard'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 200)  # Renders login page
        self.assertContains(response, 'Please log in')
    
    def test_invalid_hotel_id(self):
        """TC6.3: Invalid Hotel ID"""
        manager = User.objects.create(
            email='manager@test.com',
            password=make_password('testpass123'),
            user_role='hotel_manager'
        )
        
        self.client.post(reverse('customer_login'), {
            'email': 'manager@test.com',
            'password': 'testpass123'
        })
        
        response = self.client.get(reverse('website:edit_hotel', args=[99999]))
        
        self.assertEqual(response.status_code, 404)


class ModelTests(TestCase):
    """Test model methods and properties"""
    
    def test_user_role_methods(self):
        """Test User model role helper methods"""
        customer = User.objects.create(
            email='customer@test.com',
            password=make_password('test123'),
            user_role='customer'
        )
        
        hotel_manager = User.objects.create(
            email='hotel@test.com',
            password=make_password('test123'),
            user_role='hotel_manager'
        )
        
        transport_manager = User.objects.create(
            email='transport@test.com',
            password=make_password('test123'),
            user_role='transport_manager'
        )
        
        self.assertTrue(customer.is_customer())
        self.assertFalse(customer.is_hotel_manager())
        self.assertFalse(customer.is_transport_manager())
        
        self.assertFalse(hotel_manager.is_customer())
        self.assertTrue(hotel_manager.is_hotel_manager())
        self.assertFalse(hotel_manager.is_transport_manager())
        
        self.assertFalse(transport_manager.is_customer())
        self.assertFalse(transport_manager.is_hotel_manager())
        self.assertTrue(transport_manager.is_transport_manager())
    
    def test_hotel_str_method(self):
        """Test Hotel string representation"""
        hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Bucharest',
            address='Test Address'
        )
        
        self.assertEqual(str(hotel), 'Test Hotel — Bucharest')
    
    def test_cascade_delete_hotel_rooms(self):
        """TC8.1: Cascade Delete - Hotel with Rooms"""
        manager = User.objects.create(
            email='manager@test.com',
            password=make_password('test123'),
            user_role='hotel_manager'
        )
        
        hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Bucharest',
            address='Test Address',
            manager_user=manager
        )
        
        room = Room.objects.create(
            hotel=hotel,
            name='Test Room',
            max_persons=2,
            price_per_night=100.00,
            total_rooms=5
        )
        
        room_id = room.id
        hotel.delete()
        
        # Room should be deleted due to CASCADE
        self.assertFalse(Room.objects.filter(id=room_id).exists())


# Run all tests with:
# python manage.py test website.tests
