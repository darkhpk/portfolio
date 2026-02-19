# 🌿 Tur’Eco — Eco-Tourism Web Application

Tur’Eco is a modern **eco-tourism web platform** built with **Django**, designed to connect travelers with environmentally friendly hotels and sustainable destinations.  
The project supports **customer accounts**, **reviews**, **dark/light mode themes**, and an **admin control panel** for hotel and booking management.

---

## ✨ Features

### 👥 User System
- **Customer accounts** with email-based login and signup  
- **Admin (superuser)** accounts using Django’s built-in authentication  
- Password hashing and validation  
- Flash messages for feedback and errors  

### 🏨 Hotel Management
- View hotel details, photos, and amenities  
- Customers can **leave reviews** with ratings and eco-ratings  
- Admin/staff can **reply** to customer reviews or **add official reviews**

### 🌙 Light/Dark Mode
- Toggle between **dark** and **light** themes  
- Theme preference stored in session for each user  
- Clean, responsive UI built with custom CSS and Bootstrap-like layout

### 💬 Reviews System
- 1–5 star rating system  
- Optional **eco-rating** with leaf icons (🌿)  
- Admin/staff replies nested under customer reviews  
- Average rating automatically calculated per hotel  

### ⚙️ Admin Panel
- Manage hotels, rooms, bookings, and reviews  
- Approve or edit user-submitted reviews  
- View booking analytics and user feedback  

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 5.x (Python 3.11+) |
| **Frontend** | HTML5, CSS3, Bootstrap-like custom theme |
| **Database** | SQLite (default) or PostgreSQL |
| **Icons** | Font Awesome / Inline SVG |
| **Auth** | Django Authentication + Custom Customer Model |
| **Environment** | Python virtual environment (venv) |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tureco.git
cd tureco
