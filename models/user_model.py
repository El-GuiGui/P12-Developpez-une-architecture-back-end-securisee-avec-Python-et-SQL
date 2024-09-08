from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base
from passlib.hash import argon2


class Role(Base):
    """
    Représente un rôle utilisateur dans l'application.
    Définit les attributs et les relations pour un rôle.
    """

    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

    users = relationship("User", back_populates="role")


class User(Base):
    """
    Représente un utilisateur de l'application avec ses informations personnelles et ses relations.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(Integer, unique=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    department = Column(String)
    password_hash = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role", back_populates="users")
    clients = relationship("Client", back_populates="user")
    contracts = relationship("Contract", back_populates="user")
    events = relationship("Event", back_populates="user")

    def set_password(self, password):
        self.password_hash = argon2.hash(password)

    def check_password(self, password):
        return argon2.verify(password, self.password_hash)
