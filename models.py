from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from config import DATABASE_URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Client(Base):
    """
    Représente un client dans la base de données.
    Gère les informations de contact et les relations contractuelles.
    """

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    first_contact_date = Column(Date)
    last_contact_date = Column(Date)
    commercial_contact = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")


class Contract(Base):
    """
    Représente un contrat dans la base de données.
    Associe un client, un montant total et des événements liés.
    """

    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    commercial_contact = Column(String)
    total_amount = Column(Float)
    amount_due = Column(Float)
    creation_date = Column(Date)
    signed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    """
    Représente un événement dans la base de données.
    Associe à un contrat et à un client, avec des détails sur l'événement.
    """

    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    event_name = Column(String, index=True)
    event_date_start = Column(Date)
    event_date_end = Column(Date)
    support_contact = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(String)
    client_contact = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")


# Creation table DB
Base.metadata.create_all(bind=engine)
