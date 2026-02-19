# Demo Data Quick Reference

## 🚀 How to Populate Demo Data

Run this command in your terminal:

```powershell
cd "f:\WorkSpace\eco-turism webapp\cristi-branch\eco-turism-webapp\django_wp\tureco"
python manage.py populate_demo_data
```

## 📋 Login Credentials

### 🧑 Customer Accounts
- **Email:** `customer.demo@tureco.com` | **Password:** `demo123`
- **Email:** `sarah.demo@tureco.com` | **Password:** `demo123`

### 🏨 Hotel Manager Accounts
- **Email:** `hotelmanager.demo@tureco.com` | **Password:** `demo123`
- **Email:** `grandhotel.demo@tureco.com` | **Password:** `demo123`

### 🚌 Transport Manager Accounts
- **Email:** `transport.demo@tureco.com` | **Password:** `demo123`
- **Email:** `greentravel.demo@tureco.com` | **Password:** `demo123`

## 🏨 Demo Hotels (5 Total)

### 1. EcoLux Resort & Spa - Bucharest
- **Manager:** hotelmanager.demo@tureco.com
- **Rooms:** 
  - Deluxe Suite (2 persons) - €150/night - 10 rooms
  - Family Room (4 persons) - €220/night - 8 rooms
  - Presidential Suite (2 persons) - €350/night - 3 rooms

### 2. Green Mountain Lodge - Brasov
- **Manager:** hotelmanager.demo@tureco.com
- **Rooms:**
  - Standard Mountain View (2 persons) - €95/night - 15 rooms
  - Cabin Suite (4 persons) - €175/night - 6 rooms

### 3. Danube Eco Hotel - Constanta
- **Manager:** grandhotel.demo@tureco.com
- **Rooms:**
  - Ocean View Room (2 persons) - €120/night - 20 rooms
  - Beach Suite (3 persons) - €185/night - 10 rooms
  - Penthouse (4 persons) - €300/night - 2 rooms

### 4. Urban Green Boutique - Cluj-Napoca
- **Manager:** grandhotel.demo@tureco.com
- **Rooms:**
  - Smart Room (2 persons) - €105/night - 12 rooms
  - Terrace Suite (2 persons) - €160/night - 5 rooms

### 5. Transylvania Eco Inn - Sibiu
- **Manager:** hotelmanager.demo@tureco.com
- **Rooms:**
  - Classic Room (2 persons) - €85/night - 18 rooms
  - Heritage Suite (3 persons) - €140/night - 7 rooms

## 🚌 Demo Transportation (6 Trips)

### Buses (EcoExpress - transport.demo@tureco.com)
1. **Bucharest → Brasov** | 08:00 → 11:30 | €45/seat | 50 seats
2. **Bucharest → Cluj-Napoca** | 09:30 → 16:00 | €75/seat | 45 seats
3. **Brasov → Sibiu** | 07:30 → 10:00 | €35/seat | 48 seats
4. **Constanta → Bucharest** | 16:00 → 18:30 | €40/seat | 50 seats

### Trains (Green Railways - greentravel.demo@tureco.com)
5. **Bucharest → Constanta** | 10:15 → 12:45 | €38/seat | 120 seats
6. **Cluj-Napoca → Sibiu** | 14:00 → 17:30 | €42/seat | 100 seats

## ⭐ Demo Reviews (5 Total)
- EcoLux Resort & Spa: 2 reviews (5★ and 4★)
- Green Mountain Lodge: 1 review (5★)
- Danube Eco Hotel: 1 review (4★)
- Urban Green Boutique: 1 review (5★)

## 🎯 Presentation Scenarios

### Scenario 1: Customer Booking Flow
1. Login as `customer.demo@tureco.com`
2. Search for hotels in Bucharest
3. View EcoLux Resort & Spa details
4. Book a Deluxe Suite
5. View dashboard to see bookings

### Scenario 2: Hotel Manager Dashboard
1. Login as `hotelmanager.demo@tureco.com`
2. Access Manager Dashboard
3. View 3 managed hotels (EcoLux, Green Mountain, Transylvania)
4. Add new room type or edit existing
5. View bookings for managed hotels

### Scenario 3: Transport Manager Dashboard
1. Login as `transport.demo@tureco.com`
2. Access Manager Dashboard
3. View 4 managed bus trips
4. Add new transportation route
5. Edit existing trip details

### Scenario 4: Search & Filter
1. Search for hotels in various cities
2. Use sort by price/rating
3. Search for transportation between cities
4. Compare different transport options

## 🔄 Re-running the Command

The command clears existing demo data (accounts with "demo" in email) before adding new data, so you can run it multiple times safely.

## 🗑️ Manual Cleanup

If you want to manually remove demo data:
```python
python manage.py shell
```

```python
from website.models import User, Account
User.objects.filter(email__contains='demo').delete()
```

## 📸 Features to Demonstrate

1. ✅ Role-based registration (customer vs managers)
2. ✅ Hotel search with availability
3. ✅ Transportation search with seat availability
4. ✅ Sort by price/rating
5. ✅ Manager dashboards (separate for hotel/transport)
6. ✅ CRUD operations for managers
7. ✅ Customer reviews and ratings
8. ✅ Booking system
9. ✅ Professional home page
10. ✅ Responsive design
