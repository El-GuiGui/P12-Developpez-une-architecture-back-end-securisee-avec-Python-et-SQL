import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from models.user_model import User, Role
import config

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(setup_database):
    db = setup_database
    create_default_roles(db)

    new_user = User(employee_number=12345, full_name="bob", email="bob@bob.com", department="Commercial")
    new_user.set_password("bob123")

    role = db.query(Role).filter(Role.name == "Admin").first()
    new_user.role = role

    db.add(new_user)
    db.commit()

    user = db.query(User).filter(User.email == "bob@bob.com").first()
    assert user is not None
    assert user.check_password("bob123") == True


def create_default_roles(db):
    roles = ["Admin", "Commercial", "Support"]
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name, description=f"{role_name} role")
            db.add(role)
            db.commit()
