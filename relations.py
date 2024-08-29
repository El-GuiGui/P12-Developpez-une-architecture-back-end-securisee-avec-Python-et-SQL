from models.user_model import User
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from sqlalchemy.orm import relationship


User.clients = relationship("Client", back_populates="user")
User.contracts = relationship("Contract", back_populates="user")
User.events = relationship("Event", back_populates="user")

Client.user = relationship("User", back_populates="clients")
Contract.user = relationship("User", back_populates="contracts")
Event.user = relationship("User", back_populates="events")
