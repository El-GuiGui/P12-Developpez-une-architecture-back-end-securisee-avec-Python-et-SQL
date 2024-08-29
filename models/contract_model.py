from sqlalchemy import Column, Integer, String, ForeignKey, Float, Date, Boolean
from sqlalchemy.orm import relationship
from models.base_model import Base


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    commercial_contact = Column(String)
    total_amount = Column(Float)
    amount_due = Column(Float)
    creation_date = Column(Date)
    signed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="contracts")
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")
