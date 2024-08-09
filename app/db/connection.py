from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

class Database:
    def __init__(self, url: str, pool_size: int = 100, max_overflow: int = 10, pool_timeout: int = 30, pool_recycle: int = 1800, retries: int = 5, retry_delay: int = 5):
        self.url = url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        self.retries = retries
        self.retry_delay = retry_delay
        self.engine = self.create_engine()
        self.wait_for_db()
        self.SessionLocal = self.create_session()
        self.Base = declarative_base()

    def create_engine(self):
        return create_engine(self.url,
                             pool_size=self.pool_size,
                             max_overflow=self.max_overflow,
                             pool_timeout=self.pool_timeout,
                             pool_recycle=self.pool_recycle)

    def wait_for_db(self):
        attempts = self.retries
        while attempts > 0:
            try:
                connection = self.engine.connect()
                connection.close()
                return
            except Exception as e:
                attempts -= 1
                print(f"Database not ready, retrying... ({attempts} retries left)")
                time.sleep(self.retry_delay)
        raise Exception("Database connection failed after retries")

    def create_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

SQLALCHEMY_DATABASE_URL = 'sqlite:///dados.db'
#SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@database:5432/postgres'


db = Database(SQLALCHEMY_DATABASE_URL)
engine = Database.create_engine(db)
SessionLocal = db.SessionLocal
Base = db.Base
