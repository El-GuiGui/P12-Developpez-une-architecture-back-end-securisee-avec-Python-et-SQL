from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base_model import Base


class Event(Base):
    """
    Représente un événement dans le système, associé à un contrat et un client.
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

    user = relationship("User", back_populates="events")
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
