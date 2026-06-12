"""
Reports routes
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract
from datetime import datetime
from models import get_db, close_db, Transaction, Category, TransactionType

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/summary', methods=['GET'])
@jwt_required()
def get_summary():
    """Get financial summary"""
    user_id = get_jwt_identity()
    db = get_db()
    
    # Total income
    total_income = db.query(func.sum(Transaction.amount)).filter_by(
        user_id=user_id, type=TransactionType.INCOME
    ).scalar() or 0
    
    # Total expenses
    total_expenses = db.query(func.sum(Transaction.amount)).filter_by(
        user_id=user_id, type=TransactionType.EXPENSE
    ).scalar() or 0
    
    # Balance
    balance = total_income - total_expenses
    
    # Transaction count
    transaction_count = db.query(func.count(Transaction.id)).filter_by(user_id=user_id).scalar()
    
    close_db(db)
    
    return jsonify({
        'total_income': float(total_income),
        'total_expenses': float(total_expenses),
        'balance': float(balance),
        'transaction_count': transaction_count
    }), 200


@reports_bp.route('/by-category', methods=['GET'])
@jwt_required()
def get_by_category():
    """Get expenses/income by category"""
    user_id = get_jwt_identity()
    db = get_db()
    
    # Group by category
    results = db.query(
        Category.name,
        Category.type,
        Category.color,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    ).join(Transaction).filter(
        Transaction.user_id == user_id
    ).group_by(Category.id).all()
    
    data = []
    for row in results:
        data.append({
            'category': row.name,
            'type': row.type.value,
            'color': row.color,
            'total': float(row.total),
            'count': row.count
        })
    
    close_db(db)
    return jsonify(data), 200


@reports_bp.route('/monthly', methods=['GET'])
@jwt_required()
def get_monthly():
    """Get monthly breakdown"""
    user_id = get_jwt_identity()
    db = get_db()
    
    # Get current year
    current_year = datetime.now().year
    
    # Group by month
    results = db.query(
        extract('month', Transaction.date).label('month'),
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter(
        Transaction.user_id == user_id,
        extract('year', Transaction.date) == current_year
    ).group_by('month', Transaction.type).all()
    
    # Organize data by month
    monthly_data = {}
    for row in results:
        month_name = datetime(current_year, int(row.month), 1).strftime('%B')
        if month_name not in monthly_data:
            monthly_data[month_name] = {'income': 0, 'expenses': 0}
        
        if row.type == TransactionType.INCOME:
            monthly_data[month_name]['income'] = float(row.total)
        else:
            monthly_data[month_name]['expenses'] = float(row.total)
    
    close_db(db)
    return jsonify(monthly_data), 200
