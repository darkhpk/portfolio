"""
Database initialization
"""

from models import Base, engine, Session, User, Category, TransactionType
from werkzeug.security import generate_password_hash


def init_database():
    """Initialize database and create default data"""
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Tables created successfully!")
    
    # Create default categories
    session = Session()
    
    # Check if default categories exist
    if session.query(Category).count() == 0:
        print("Creating default categories...")
        
        # Demo user
        demo_user = User(
            username='demo',
            email='demo@example.com',
            password_hash=generate_password_hash('demo123')
        )
        session.add(demo_user)
        session.flush()
        
        default_categories = [
            # Expense categories
            {'name': 'Food & Dining', 'type': TransactionType.EXPENSE, 'color': '#e74c3c', 'user_id': demo_user.id},
            {'name': 'Transportation', 'type': TransactionType.EXPENSE, 'color': '#3498db', 'user_id': demo_user.id},
            {'name': 'Shopping', 'type': TransactionType.EXPENSE, 'color': '#9b59b6', 'user_id': demo_user.id},
            {'name': 'Entertainment', 'type': TransactionType.EXPENSE, 'color': '#f39c12', 'user_id': demo_user.id},
            {'name': 'Bills & Utilities', 'type': TransactionType.EXPENSE, 'color': '#34495e', 'user_id': demo_user.id},
            {'name': 'Healthcare', 'type': TransactionType.EXPENSE, 'color': '#16a085', 'user_id': demo_user.id},
            {'name': 'Education', 'type': TransactionType.EXPENSE, 'color': '#2ecc71', 'user_id': demo_user.id},
            
            # Income categories
            {'name': 'Salary', 'type': TransactionType.INCOME, 'color': '#27ae60', 'user_id': demo_user.id},
            {'name': 'Freelance', 'type': TransactionType.INCOME, 'color': '#2ecc71', 'user_id': demo_user.id},
            {'name': 'Investment', 'type': TransactionType.INCOME, 'color': '#1abc9c', 'user_id': demo_user.id},
            {'name': 'Other Income', 'type': TransactionType.INCOME, 'color': '#16a085', 'user_id': demo_user.id},
        ]
        
        for cat_data in default_categories:
            category = Category(**cat_data)
            session.add(category)
        
        session.commit()
        print("Default categories created!")
        print("Demo account created - username: demo, password: demo123")
    
    session.close()
    print("Database initialization complete!")


if __name__ == '__main__':
    init_database()
