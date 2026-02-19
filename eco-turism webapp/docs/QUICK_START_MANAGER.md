# Quick Start Guide - Manager System

## ⚡ Quick Setup (3 Steps)

### Step 1: Run Database Migrations
```powershell
cd "f:\WorkSpace\eco-turism webapp\cristi-branch\eco-turism-webapp\django_wp\tureco"
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Test the System
1. Go to signup page: http://localhost:8000/customer/signup/
2. Choose "Hotel Manager" or "Transport Manager"
3. Create account and login
4. You'll be redirected to Manager Dashboard

### Step 3: Add Your First Listing
**For Hotel Managers:**
- Click "Add New Hotel"
- Fill in hotel details
- After saving, click "Add Room" to add room types

**For Transport Managers:**
- Click "Add New Trip"  
- Fill in route, schedule, pricing
- Save and it's live!

---

## 🎯 What Was Added

### ✅ Registration Page
- Radio buttons to select account type
- Customer, Hotel Manager, or Transport Manager

### ✅ Manager Dashboard
- **Hotel Managers** see list of their hotels with actions
- **Transport Managers** see list of their trips with actions
- Add, Edit, Delete functionality for all listings

### ✅ Hotel Management
- Add hotels with full details
- Add multiple room types per hotel
- Edit existing hotels
- Delete with confirmation

### ✅ Transportation Management
- Add bus/train/flight services
- Set routes, schedules, pricing
- Edit existing trips
- Delete with confirmation

---

## 🔗 Important URLs

| Feature | URL |
|---------|-----|
| Sign Up | `/customer/signup/` |
| Login | `/customer/login/` |
| Manager Dashboard | `/manager/dashboard/` |
| Add Hotel | `/manager/hotel/add/` |
| Add Transportation | `/manager/transportation/add/` |

---

## 🛡️ Security

- ✅ Managers can only manage their OWN listings
- ✅ Customers cannot access manager pages
- ✅ Session validation on all pages
- ✅ Confirmation dialogs for deletions

---

## 📱 How Customers See It

- Customers search and see ALL hotels (including manager-added)
- Customers search and see ALL transportation (including manager-added)
- Booking works exactly the same
- Reviews work on manager hotels

---

## 🎨 UI Features

- Modern Bootstrap 5 design
- Responsive tables
- Icon-based navigation
- Color-coded status badges
- Professional forms with validation
- Helpful error messages

---

## ✨ Example Workflow

### Hotel Manager Flow:
1. Register as Hotel Manager → Login
2. Click "Add New Hotel" → Fill form → Save
3. Click "Add Room" next to hotel → Add "Standard Room" for €99/night
4. Click "Add Room" again → Add "Deluxe Suite" for €199/night
5. Customers can now search and book your hotel!

### Transport Manager Flow:
1. Register as Transport Manager → Login
2. Click "Add New Trip" → Select "Bus"
3. Set route: "Bucharest" → "Cluj-Napoca"
4. Set departure/arrival times
5. Set 50 seats at €29/seat → Save
6. Customers can now search and book seats!

---

## 🐛 Troubleshooting

**Problem:** Can't see manager dashboard after login
**Solution:** Make sure you selected "Hotel Manager" or "Transport Manager" during signup

**Problem:** Getting "Only managers can add hotels" error
**Solution:** You registered as Customer - create new account as Manager

**Problem:** Can't edit someone else's hotel
**Solution:** Working as intended! You can only edit your own properties

**Problem:** Changes not showing
**Solution:** Run migrations: `python manage.py makemigrations && python manage.py migrate`

---

## 📞 Support

Check `MANAGER_FEATURE_DOCUMENTATION.md` for complete details on all features.
