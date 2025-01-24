from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

DATABASE_URL = os.environ.get("DATABASE_CONNECTION_STRING")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.current_date())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
