from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time



def wait_for_db(engine):
    retries = 5
    while retries > 0:
        try:
            connection = engine.connect()
            connection.close()
            return
        except Exception as e:
            retries -= 1
            print(f"Database not ready, retrying... ({retries} retries left)")
            time.sleep(5)

SQLALCHEMY_DATABASE_URL = 'sqlite:///dados.db'
# SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@localhost:5432/postgres'


engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=100,
                       max_overflow=10,
                       pool_timeout=30,
                       pool_recycle=1800)

wait_for_db(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()