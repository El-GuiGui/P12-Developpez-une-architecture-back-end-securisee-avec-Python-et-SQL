from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base
from datetime import datetime


class Client(Base):
    """
    Représente un client dans le système, avec ses informations de contact et ses relations.
    """

    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    first_contact_date = Column(Date, default=datetime.utcnow)
    last_contact_date = Column(Date, default=datetime.utcnow)
    commercial_contact = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")
    events = relationship("Event", back_populates="client")
