from db.models import Base
from db.engine import Engine


def setup_database():
    Base.metadata.create_all(Engine)
