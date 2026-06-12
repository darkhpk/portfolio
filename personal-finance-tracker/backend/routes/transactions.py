"""
Transaction routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import get_db, close_db, Transaction, Category

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def list_transactions():
    """List all transactions for current user"""
    user_id = get_jwt_identity()
    db = get_db()
    
    transactions = db.query(Transaction).filter_by(user_id=user_id).order_by(Transaction.date.desc()).all()
    
    result = []
    for trans in transactions:
        category_name = trans.category.name if trans.category else None
        result.append({
            'id': trans.id,
            'amount': trans.amount,
            'type': trans.type.value,
            'description': trans.description,
            'date': trans.date.isoformat(),
            'category_id': trans.category_id,
            'category_name': category_name,
            'created_at': trans.created_at.isoformat()
        })
    
    close_db(db)
    return jsonify(result), 200


@transactions_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    """Get specific transaction"""
    user_id = get_jwt_identity()
    db = get_db()
    
    trans = db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
    if not trans:
        close_db(db)
        return jsonify({'error': 'Transaction not found'}), 404
    
    result = {
        'id': trans.id,
        'amount': trans.amount,
        'type': trans.type.value,
        'description': trans.description,
        'date': trans.date.isoformat(),
        'category_id': trans.category_id,
        'created_at': trans.created_at.isoformat()
    }
    
    close_db(db)
    return jsonify(result), 200


@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create new transaction"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('amount') or not data.get('type') or not data.get('date'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    
    new_transaction = Transaction(
        amount=data['amount'],
        type=data['type'],
        description=data.get('description', ''),
        date=datetime.fromisoformat(data['date'].replace('Z', '+00:00')),
        category_id=data.get('category_id'),
        user_id=user_id
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    trans_id = new_transaction.id
    close_db(db)
    
    return jsonify({'message': 'Transaction created', 'id': trans_id}), 201


@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """Update transaction"""
    user_id = get_jwt_identity()
    data = request.get_json()
    db = get_db()
    
    trans = db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
    if not trans:
        close_db(db)
        return jsonify({'error': 'Transaction not found'}), 404
    
    if 'amount' in data:
        trans.amount = data['amount']
    if 'type' in data:
        trans.type = data['type']
    if 'description' in data:
        trans.description = data['description']
    if 'date' in data:
        trans.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
    if 'category_id' in data:
        trans.category_id = data['category_id']
    
    db.commit()
    close_db(db)
    
    return jsonify({'message': 'Transaction updated'}), 200


@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    """Delete transaction"""
    user_id = get_jwt_identity()
    db = get_db()
    
    trans = db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
    if not trans:
        close_db(db)
        return jsonify({'error': 'Transaction not found'}), 404
    
    db.delete(trans)
    db.commit()
    close_db(db)
    
    return jsonify({'message': 'Transaction deleted'}), 200
