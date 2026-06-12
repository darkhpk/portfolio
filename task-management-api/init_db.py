"""
Database initialization script
"""

from app.db.database import engine, Base
from app.models import user, task, project


def init_database():
    """Initialize database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_database()
