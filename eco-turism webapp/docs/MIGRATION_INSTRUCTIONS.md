# Database Migration Instructions

## You need to run these commands to apply the database changes:

```powershell
# Navigate to the project directory
cd "f:\WorkSpace\eco-turism webapp\cristi-branch\eco-turism-webapp\django_wp\tureco"

# Create migration file
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

## What changed:
1. Added `user_role` field to User model (customer, hotel_manager, transport_manager)
2. Added `manager_user` field to Hotel model (tracks which manager owns the hotel)
3. Added `manager_user` field to TransportationTrip model (tracks which manager owns the transportation)

## After migration, you can:
- Register as a Hotel Manager or Transport Manager
- Managers can add/edit/delete their hotels and rooms
- Transport managers can add/edit/delete transportation services
- Customers continue to book as normal
