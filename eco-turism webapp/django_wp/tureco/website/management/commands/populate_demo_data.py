"""
Django management command to populate database with demo data
Usage: python manage.py populate_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta, date
from website.models import (
    User, Account, Hotel, Room, 
    TransportationTrip, Review
)


class Command(BaseCommand):
    help = 'Populates the database with demo data for presentations'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting demo data population...'))

        # Clear existing demo data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing demo data...')
        User.objects.filter(email__contains='demo').delete()
        Account.objects.filter(user_id__email__contains='demo').delete()
        
        # Create Demo User Accounts
        self.stdout.write(self.style.WARNING('\n📧 Creating Demo User Accounts...'))
        
        # Customer users
        customer1 = User.objects.create(
            email='customer.demo@tureco.com',
            password=make_password('demo123'),
            user_role='customer'
        )
        # Create Account for customer1
        account1 = Account.objects.create(
            user_id=customer1,
            fname='John',
            lname='Smith',
            phone='+40721234567',
            dateofbirth=date(1990, 5, 15)
        )
        self.stdout.write(f'✅ Customer: {customer1.email} / demo123')
        
        customer2 = User.objects.create(
            email='sarah.demo@tureco.com',
            password=make_password('demo123'),
            user_role='customer'
        )
        # Create Account for customer2
        account2 = Account.objects.create(
            user_id=customer2,
            fname='Sarah',
            lname='Johnson',
            phone='+40722345678',
            dateofbirth=date(1988, 8, 22)
        )
        self.stdout.write(f'✅ Customer: {customer2.email} / demo123')
        
        # Manager accounts (User model)
        hotel_manager1 = User.objects.create(
            email='hotelmanager.demo@tureco.com',
            password=make_password('demo123'),
            user_role='hotel_manager'
        )
        self.stdout.write(f'✅ Hotel Manager: {hotel_manager1.email} / demo123')
        
        hotel_manager2 = User.objects.create(
            email='grandhotel.demo@tureco.com',
            password=make_password('demo123'),
            user_role='hotel_manager'
        )
        self.stdout.write(f'✅ Hotel Manager: {hotel_manager2.email} / demo123')
        
        transport_manager1 = User.objects.create(
            email='transport.demo@tureco.com',
            password=make_password('demo123'),
            user_role='transport_manager'
        )
        self.stdout.write(f'✅ Transport Manager: {transport_manager1.email} / demo123')
        
        transport_manager2 = User.objects.create(
            email='greentravel.demo@tureco.com',
            password=make_password('demo123'),
            user_role='transport_manager'
        )
        self.stdout.write(f'✅ Transport Manager: {transport_manager2.email} / demo123')

        # Create Demo Hotels
        self.stdout.write(self.style.WARNING('\n🏨 Creating Demo Hotels...'))
        
        hotel1 = Hotel.objects.create(
            name='EcoLux Resort & Spa',
            city='Bucharest',
            address='Calea Victoriei 125, Bucharest 010071',
            description='A luxury eco-resort in the heart of Bucharest featuring solar panels, rainwater harvesting, and locally sourced organic cuisine. Our commitment to sustainability meets 5-star comfort.',
            thumbnail_url='https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
            tags='luxury, spa, organic, solar-powered',
            manager_user=hotel_manager1
        )
        Room.objects.create(hotel=hotel1, name='Deluxe Suite', max_persons=2, price_per_night=150.00, total_rooms=10)
        Room.objects.create(hotel=hotel1, name='Family Room', max_persons=4, price_per_night=220.00, total_rooms=8)
        Room.objects.create(hotel=hotel1, name='Presidential Suite', max_persons=2, price_per_night=350.00, total_rooms=3)
        self.stdout.write(f'✅ Hotel: {hotel1.name} (3 room types)')
        
        hotel2 = Hotel.objects.create(
            name='Green Mountain Lodge',
            city='Brasov',
            address='Strada Poiana Brasov 15, Brasov 500001',
            description='Nestled in the Carpathian Mountains, our eco-lodge is built with sustainable materials and powered by renewable energy. Perfect for nature lovers and adventure seekers.',
            thumbnail_url='https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
            tags='mountain, eco-friendly, adventure, nature',
            manager_user=hotel_manager1
        )
        Room.objects.create(hotel=hotel2, name='Standard Mountain View', max_persons=2, price_per_night=95.00, total_rooms=15)
        Room.objects.create(hotel=hotel2, name='Cabin Suite', max_persons=4, price_per_night=175.00, total_rooms=6)
        self.stdout.write(f'✅ Hotel: {hotel2.name} (2 room types)')
        
        hotel3 = Hotel.objects.create(
            name='Danube Eco Hotel',
            city='Constanta',
            address='Bulevardul Mamaia 255, Constanta 900001',
            description='Beachfront hotel with zero-waste commitment, electric vehicle charging stations, and biodegradable amenities. Experience the Black Sea coast sustainably.',
            thumbnail_url='https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
            tags='beach, zero-waste, seaside, modern',
            manager_user=hotel_manager2
        )
        Room.objects.create(hotel=hotel3, name='Ocean View Room', max_persons=2, price_per_night=120.00, total_rooms=20)
        Room.objects.create(hotel=hotel3, name='Beach Suite', max_persons=3, price_per_night=185.00, total_rooms=10)
        Room.objects.create(hotel=hotel3, name='Penthouse', max_persons=4, price_per_night=300.00, total_rooms=2)
        self.stdout.write(f'✅ Hotel: {hotel3.name} (3 room types)')
        
        hotel4 = Hotel.objects.create(
            name='Urban Green Boutique',
            city='Cluj-Napoca',
            address='Piata Unirii 22, Cluj-Napoca 400000',
            description='Modern boutique hotel in the city center with rooftop garden, bike rentals, and farm-to-table restaurant. Urban comfort with environmental consciousness.',
            thumbnail_url='https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
            tags='boutique, urban, rooftop, bike-friendly',
            manager_user=hotel_manager2
        )
        Room.objects.create(hotel=hotel4, name='Smart Room', max_persons=2, price_per_night=105.00, total_rooms=12)
        Room.objects.create(hotel=hotel4, name='Terrace Suite', max_persons=2, price_per_night=160.00, total_rooms=5)
        self.stdout.write(f'✅ Hotel: {hotel4.name} (2 room types)')
        
        hotel5 = Hotel.objects.create(
            name='Transylvania Eco Inn',
            city='Sibiu',
            address='Strada Cetatii 8, Sibiu 550160',
            description='Historic building renovated with eco-friendly materials, geothermal heating, and traditional Romanian hospitality. Discover medieval Sibiu sustainably.',
            thumbnail_url='https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
            tags='historic, traditional, geothermal, cultural',
            manager_user=hotel_manager1
        )
        Room.objects.create(hotel=hotel5, name='Classic Room', max_persons=2, price_per_night=85.00, total_rooms=18)
        Room.objects.create(hotel=hotel5, name='Heritage Suite', max_persons=3, price_per_night=140.00, total_rooms=7)
        self.stdout.write(f'✅ Hotel: {hotel5.name} (2 room types)')

        # Create Demo Transportation
        self.stdout.write(self.style.WARNING('\n🚌 Creating Demo Transportation...'))
        
        # Buses
        base_date = datetime.now() + timedelta(days=2)
        
        trip1 = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='EcoExpress',
            origin_city='Bucharest',
            destination_city='Brasov',
            departure=base_date.replace(hour=8, minute=0),
            arrival=base_date.replace(hour=11, minute=30),
            car_reg='B-ECO-001',
            total_seats=50,
            price_per_seat=45.00,
            thumbnail_url='https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800',
            manager_user=transport_manager1
        )
        self.stdout.write(f'✅ Bus: {trip1.origin_city} → {trip1.destination_city} ({trip1.departure.strftime("%Y-%m-%d %H:%M")})')
        
        trip2 = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='EcoExpress',
            origin_city='Bucharest',
            destination_city='Cluj-Napoca',
            departure=base_date.replace(hour=9, minute=30),
            arrival=base_date.replace(hour=16, minute=0),
            car_reg='B-ECO-002',
            total_seats=45,
            price_per_seat=75.00,
            thumbnail_url='https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800',
            manager_user=transport_manager1
        )
        self.stdout.write(f'✅ Bus: {trip2.origin_city} → {trip2.destination_city} ({trip2.departure.strftime("%Y-%m-%d %H:%M")})')
        
        # Trains
        trip3 = TransportationTrip.objects.create(
            transport_type='train',
            operator_name='Green Railways',
            origin_city='Bucharest',
            destination_city='Constanta',
            departure=(base_date + timedelta(days=1)).replace(hour=10, minute=15),
            arrival=(base_date + timedelta(days=1)).replace(hour=12, minute=45),
            car_reg='CFR-2024-A1',
            total_seats=120,
            price_per_seat=38.00,
            thumbnail_url='https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800',
            manager_user=transport_manager2
        )
        self.stdout.write(f'✅ Train: {trip3.origin_city} → {trip3.destination_city} ({trip3.departure.strftime("%Y-%m-%d %H:%M")})')
        
        trip4 = TransportationTrip.objects.create(
            transport_type='train',
            operator_name='Green Railways',
            origin_city='Cluj-Napoca',
            destination_city='Sibiu',
            departure=(base_date + timedelta(days=1)).replace(hour=14, minute=0),
            arrival=(base_date + timedelta(days=1)).replace(hour=17, minute=30),
            car_reg='CFR-2024-B2',
            total_seats=100,
            price_per_seat=42.00,
            thumbnail_url='https://images.unsplash.com/photo-1474487548417-781cb71495f3?w=800',
            manager_user=transport_manager2
        )
        self.stdout.write(f'✅ Train: {trip4.origin_city} → {trip4.destination_city} ({trip4.departure.strftime("%Y-%m-%d %H:%M")})')
        
        trip5 = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='EcoExpress',
            origin_city='Brasov',
            destination_city='Sibiu',
            departure=(base_date + timedelta(days=2)).replace(hour=7, minute=30),
            arrival=(base_date + timedelta(days=2)).replace(hour=10, minute=0),
            car_reg='B-ECO-003',
            total_seats=48,
            price_per_seat=35.00,
            thumbnail_url='https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800',
            manager_user=transport_manager1
        )
        self.stdout.write(f'✅ Bus: {trip5.origin_city} → {trip5.destination_city} ({trip5.departure.strftime("%Y-%m-%d %H:%M")})')
        
        trip6 = TransportationTrip.objects.create(
            transport_type='bus',
            operator_name='EcoExpress',
            origin_city='Constanta',
            destination_city='Bucharest',
            departure=(base_date + timedelta(days=3)).replace(hour=16, minute=0),
            arrival=(base_date + timedelta(days=3)).replace(hour=18, minute=30),
            car_reg='B-ECO-004',
            total_seats=50,
            price_per_seat=40.00,
            thumbnail_url='https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=800',
            manager_user=transport_manager1
        )
        self.stdout.write(f'✅ Bus: {trip6.origin_city} → {trip6.destination_city} ({trip6.departure.strftime("%Y-%m-%d %H:%M")})')

        # Create Demo Reviews
        self.stdout.write(self.style.WARNING('\n⭐ Creating Demo Reviews...'))
        
        Review.objects.create(
            hotel_id=hotel1,
            account_id=account1,
            rating=5,
            eco_rating=5,
            comment='Amazing eco-friendly resort! The solar panels and organic restaurant exceeded our expectations. Highly recommend!'
        )
        
        Review.objects.create(
            hotel_id=hotel1,
            account_id=account2,
            rating=4,
            eco_rating=5,
            comment='Great location and excellent sustainability practices. The spa was wonderful.'
        )
        
        Review.objects.create(
            hotel_id=hotel2,
            account_id=account1,
            rating=5,
            eco_rating=4,
            comment='Perfect mountain getaway! The eco-lodge is beautiful and the staff is very knowledgeable about local nature.'
        )
        
        Review.objects.create(
            hotel_id=hotel3,
            account_id=account2,
            rating=4,
            eco_rating=5,
            comment='Love the zero-waste commitment! Beach was clean and the EV charging station was very convenient.'
        )
        
        Review.objects.create(
            hotel_id=hotel4,
            account_id=account1,
            rating=5,
            eco_rating=4,
            comment='Modern, clean, and green! The rooftop garden and bike rentals made our city tour amazing.'
        )
        
        self.stdout.write(f'✅ Created 5 demo reviews')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✅ DEMO DATA POPULATED SUCCESSFULLY!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        self.stdout.write(self.style.WARNING('\n📋 LOGIN CREDENTIALS:'))
        self.stdout.write('\n🧑 CUSTOMERS:')
        self.stdout.write('  Email: customer.demo@tureco.com | Password: demo123')
        self.stdout.write('  Email: sarah.demo@tureco.com    | Password: demo123')
        
        self.stdout.write('\n🏨 HOTEL MANAGERS:')
        self.stdout.write('  Email: hotelmanager.demo@tureco.com | Password: demo123')
        self.stdout.write('  Email: grandhotel.demo@tureco.com   | Password: demo123')
        
        self.stdout.write('\n🚌 TRANSPORT MANAGERS:')
        self.stdout.write('  Email: transport.demo@tureco.com   | Password: demo123')
        self.stdout.write('  Email: greentravel.demo@tureco.com | Password: demo123')
        
        self.stdout.write(self.style.WARNING('\n📊 DATA SUMMARY:'))
        self.stdout.write(f'  • 2 Customer Accounts')
        self.stdout.write(f'  • 2 Hotel Manager Accounts')
        self.stdout.write(f'  • 2 Transport Manager Accounts')
        self.stdout.write(f'  • 5 Hotels with 12 room types')
        self.stdout.write(f'  • 6 Transportation trips')
        self.stdout.write(f'  • 5 Reviews')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 Ready for your presentation!\n'))
