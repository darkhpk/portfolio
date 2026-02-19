# Role-Based Registration System - Feature Documentation

## Overview
Implemented a complete role-based registration system that allows users to register as **Customers**, **Hotel Managers**, or **Transport Managers**. Managers can add, edit, and delete their own hotels/transportation services.

---

## 🎯 Key Features

### 1. **Role-Based Registration**
- Users can choose their account type during signup:
  - **Customer** - Book hotels and transportation
  - **Hotel Manager** - Manage hotel listings and rooms
  - **Transport Manager** - Manage transportation services

### 2. **Manager Dashboard**
- Dedicated dashboard for hotel and transport managers
- View all managed properties/services
- Quick actions: Add, Edit, Delete, View

### 3. **Hotel Management** (Hotel Managers)
- ✅ Add new hotels with details (name, city, address, description, images, tags)
- ✅ Add room types to hotels (name, capacity, price, quantity)
- ✅ Edit existing hotel information
- ✅ Delete hotels (with confirmation)
- ✅ View all bookings for managed hotels

### 4. **Transportation Management** (Transport Managers)
- ✅ Add transportation services (bus, train, flight)
- ✅ Set routes, schedules, pricing, and capacity
- ✅ Edit existing transportation services
- ✅ Delete transportation (with confirmation)
- ✅ Track bookings for managed services

---

## 📁 Files Modified

### Models (`models.py`)
```python
class User:
    - Added: user_role field (customer, hotel_manager, transport_manager)
    - Added: Helper methods (is_customer, is_hotel_manager, is_transport_manager)

class Hotel:
    - Added: manager_user field (ForeignKey to User)
    
class TransportationTrip:
    - Added: manager_user field (ForeignKey to User)
```

### Forms (`forms.py`)
```python
- Updated: CustomerSignupForm (added role selection)
- Added: AddHotelForm
- Added: AddRoomForm
- Added: AddTransportationForm
```

### Views (`views.py`)
```python
- Added: manager_login_required decorator
- Added: manager_dashboard
- Added: add_hotel, edit_hotel, delete_hotel
- Added: add_room
- Added: add_transportation, edit_transportation, delete_transportation
- Updated: customer_dashboard (redirects managers to manager dashboard)
```

### URLs (`urls.py`)
```python
New routes:
- /manager/dashboard/
- /manager/hotel/add/
- /manager/hotel/<id>/edit/
- /manager/hotel/<id>/delete/
- /manager/hotel/<id>/room/add/
- /manager/transportation/add/
- /manager/transportation/<id>/edit/
- /manager/transportation/<id>/delete/
```

### Templates
```
New templates created:
- templates/manager/dashboard.html
- templates/manager/add_hotel.html
- templates/manager/add_room.html
- templates/manager/edit_hotel.html
- templates/manager/add_transportation.html
- templates/manager/edit_transportation.html
- templates/manager/confirm_delete.html

Updated:
- templates/booking/customer_signup.html (role selection UI)
```

---

## 🚀 Usage Instructions

### For Hotel Managers:
1. Register as "Hotel Manager"
2. Login and you'll be redirected to Manager Dashboard
3. Click "Add New Hotel" to create your first hotel
4. After adding hotel, click "Add Room" to add room types
5. Edit or delete hotels/rooms as needed
6. Customers can search and book your rooms

### For Transport Managers:
1. Register as "Transport Manager"
2. Login and you'll be redirected to Manager Dashboard
3. Click "Add New Trip" to create transportation service
4. Fill in route, schedule, pricing, and capacity
5. Edit or delete trips as needed
6. Customers can search and book seats

### For Customers:
1. Register as "Customer" (default)
2. Login to search and book hotels/transportation
3. View bookings in Customer Dashboard
4. Leave reviews on hotels

---

## 🔒 Security Features

1. **Role-based access control**
   - Managers can only manage their own properties
   - Customers cannot access manager functions
   - Proper authentication checks on all manager views

2. **Session validation**
   - All views check for valid user sessions
   - Expired sessions redirect to login

3. **Ownership verification**
   - Managers can only edit/delete their own hotels/trips
   - Database queries filtered by manager_user

---

## 📊 Database Changes

**You must run migrations before using this feature:**

```bash
python manage.py makemigrations
python manage.py migrate
```

**Changes:**
1. User model: Added `user_role` field
2. Hotel model: Added `manager_user` field
3. TransportationTrip model: Added `manager_user` field

---

## 🎨 UI/UX Highlights

- **Modern Bootstrap 5 design** matching existing pages
- **Icon-based navigation** (Font Awesome)
- **Responsive tables** for managing listings
- **Color-coded badges** for status indicators
- **Confirmation dialogs** for destructive actions
- **Form validation** with helpful error messages
- **Intuitive workflow** from registration to management

---

## 🧪 Testing Checklist

- [ ] Register as customer
- [ ] Register as hotel manager
- [ ] Register as transport manager
- [ ] Hotel manager can add hotel
- [ ] Hotel manager can add rooms to hotel
- [ ] Hotel manager can edit hotel
- [ ] Hotel manager can delete hotel
- [ ] Transport manager can add transportation
- [ ] Transport manager can edit transportation
- [ ] Transport manager can delete transportation
- [ ] Customers can see and book manager-added hotels
- [ ] Customers can see and book manager-added transportation
- [ ] Managers cannot edit other managers' properties
- [ ] Customer dashboard still works for customers
- [ ] Manager dashboard shows correct information

---

## 🔄 Integration with Existing Features

✅ Works seamlessly with existing booking system
✅ Reviews work on manager-added hotels
✅ Search finds manager-added hotels and transportation
✅ Booking confirmations work for manager properties
✅ Customer dashboard unaffected
✅ Admin panel can still manage all data

---

## 💡 Future Enhancements (Optional)

- Booking management for managers (view/cancel bookings)
- Revenue reports and analytics
- Manager profile pages
- Bulk upload for multiple hotels/trips
- Email notifications for new bookings
- Rating system for managers
- Manager verification/approval system
- Multi-image upload for hotels
- Calendar view for transportation schedules

---

## 📝 Notes

- Existing users in database will default to 'customer' role
- Managers see their dashboard automatically upon login
- Customers continue using the system as before
- All manager functions require authentication
- Forms include proper validation and error handling
- Delete operations include safety confirmations
