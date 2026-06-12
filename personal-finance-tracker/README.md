# Personal Finance Tracker

A full-stack web application for tracking personal finances with React frontend and Flask backend. Features expense tracking, budget management, and financial insights with interactive charts.

## Features

### Frontend (React)
- **Dashboard**: Overview of financial status
- **Expense Tracking**: Add, edit, and categorize expenses
- **Income Management**: Track multiple income sources
- **Budget Planning**: Set and monitor budgets by category
- **Reports**: Visual reports with charts and graphs
- **Responsive Design**: Mobile-friendly interface

### Backend (Flask)
- **RESTful API**: Clean API endpoints
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: User authentication system
- **Data Analysis**: Financial statistics and insights
- **CSV Export**: Export data for external analysis

## Technologies Used

### Frontend
- React 18
- React Router - Navigation
- Axios - HTTP client
- Chart.js - Data visualization
- Material-UI - UI components
- CSS3 - Styling

### Backend
- Flask - Web framework
- SQLAlchemy - ORM
- Flask-JWT-Extended - Authentication
- Flask-CORS - Cross-origin support
- pandas - Data analysis

## Installation

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_db.py
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## Usage

1. Register a new account
2. Login to access the dashboard
3. Add your expenses and income
4. Set budgets for different categories
5. View reports and insights

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Transactions
- `GET /api/transactions` - List all transactions
- `GET /api/transactions/{id}` - Get specific transaction
- `POST /api/transactions` - Create transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category

### Reports
- `GET /api/reports/summary` - Financial summary
- `GET /api/reports/monthly` - Monthly breakdown
- `GET /api/reports/by-category` - Category analysis

## Project Structure

```
personal-finance-tracker/
├── backend/
│   ├── app.py              # Flask application
│   ├── init_db.py          # Database initialization
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   └── utils/              # Utility functions
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.js          # Main app component
│   └── package.json
└── README.md
```

## Features in Detail

### Expense Categories
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Education
- Others (Custom categories)

### Reports & Analytics
- Monthly spending trends
- Category-wise breakdown
- Budget vs. Actual comparison
- Income vs. Expenses
- Savings rate

## Future Enhancements

- Recurring transactions
- Multi-currency support
- Bank account integration
- Receipt scanning (OCR)
- Financial goal setting
- Investment tracking
- Mobile app
