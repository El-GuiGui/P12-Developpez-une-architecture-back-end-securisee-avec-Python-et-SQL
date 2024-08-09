from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle
from sqlalchemy import Column, Integer, String


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    first_contact_date = Column(String)
    last_contact_date = Column(String)
    commercial_contact = Column(String)


# Création des tables dans la db
Base.metadata.create_all(bind=engine)
