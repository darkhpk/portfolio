"""
Category routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_db, close_db, Category

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/', methods=['GET'])
@jwt_required()
def list_categories():
    """List all categories for current user"""
    user_id = get_jwt_identity()
    db = get_db()
    
    categories = db.query(Category).filter_by(user_id=user_id).all()
    
    result = []
    for cat in categories:
        result.append({
            'id': cat.id,
            'name': cat.name,
            'type': cat.type.value,
            'color': cat.color,
            'created_at': cat.created_at.isoformat()
        })
    
    close_db(db)
    return jsonify(result), 200


@categories_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    """Create new category"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('type'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    
    new_category = Category(
        name=data['name'],
        type=data['type'],
        color=data.get('color', '#3498db'),
        user_id=user_id
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    cat_id = new_category.id
    close_db(db)
    
    return jsonify({'message': 'Category created', 'id': cat_id}), 201
