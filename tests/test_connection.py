from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        print("Connection to the database was successful!")
except Exception as e:
    print(f"An error occurred: {e}")
