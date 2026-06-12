"""
Personal Finance Tracker - Flask Backend
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.transactions import transactions_bp
from routes.categories import categories_bp
from routes.reports import reports_bp
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
app.register_blueprint(categories_bp, url_prefix='/api/categories')
app.register_blueprint(reports_bp, url_prefix='/api/reports')


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Personal Finance Tracker API',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'transactions': '/api/transactions',
            'categories': '/api/categories',
            'reports': '/api/reports'
        }
    })


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


if __name__ == '__main__':
    print("=" * 60)
    print("Personal Finance Tracker API")
    print("=" * 60)
    print("Server starting at http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
