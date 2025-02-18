from .user import Base
from config import engine, SessionLocal

def init_db():
    Base.metadata.create_all(engine)