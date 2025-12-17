from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = scoped_session(sessionmaker(bind=engine))

def init_db():
    Base.metadata.create_all(engine)

def get_session():
    return SessionLocal()

def close_session():
    SessionLocal.remove()
