from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Replace with your actual PostgreSQL credentials
DATABASE_URL = "postgresql+psycopg2://postgres:your_password@localhost:5432/garage"

# Create engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# Create tables if they don't exist (optional for dev, Alembic preferred in prod)
def init_db():
    Base.metadata.create_all(bind=engine)
