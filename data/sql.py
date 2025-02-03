from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base

engine = create_engine('mysql://user:pass@localhost/job_db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True)