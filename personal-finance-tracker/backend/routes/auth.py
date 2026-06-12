"""
Authentication routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db, close_db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    db = get_db()
    
    # Check if user exists
    if db.query(User).filter_by(username=data['username']).first():
        close_db(db)
        return jsonify({'error': 'Username already exists'}), 400
    
    if db.query(User).filter_by(email=data['email']).first():
        close_db(db)
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    user_id = new_user.id
    close_db(db)
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user_id
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400
    
    db = get_db()
    user = db.query(User).filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        close_db(db)
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    result = {
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }
    
    close_db(db)
    return jsonify(result), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user info"""
    user_id = get_jwt_identity()
    db = get_db()
    
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        close_db(db)
        return jsonify({'error': 'User not found'}), 404
    
    result = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }
    
    close_db(db)
    return jsonify(result), 200
