from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL, DEBUG

Engine = create_engine(DATABASE_URL, echo=DEBUG)

Session = sessionmaker(bind=Engine)
