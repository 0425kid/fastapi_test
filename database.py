from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL database URL (replace with your actual database URL)
DATABASE_URL = "postgresql://myuser:password@localhost/mydatabase"

# SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# SQLAlchemy session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
