"""
Database models
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()
engine = create_engine('sqlite:///finance.db')
Session = sessionmaker(bind=engine)


class TransactionType(str, enum.Enum):
    """Transaction type enumeration"""
    INCOME = "income"
    EXPENSE = "expense"


class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship('Transaction', back_populates='user', cascade='all, delete-orphan')
    categories = relationship('Category', back_populates='user', cascade='all, delete-orphan')


class Category(Base):
    """Category model"""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    color = Column(String(7), default='#3498db')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='categories')
    transactions = relationship('Transaction', back_populates='category')


class Transaction(Base):
    """Transaction model"""
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    description = Column(String(200))
    date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')


def get_db():
    """Get database session"""
    db = Session()
    try:
        return db
    finally:
        pass


def close_db(db):
    """Close database session"""
    db.close()
