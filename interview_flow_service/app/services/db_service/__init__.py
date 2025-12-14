from .main import DBService
from functools import lru_cache

@lru_cache()
def get_db()->DBService:
    return DBService()