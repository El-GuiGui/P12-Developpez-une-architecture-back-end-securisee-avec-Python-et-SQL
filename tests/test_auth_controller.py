import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from controllers.auth_controller import AuthController
from models.base_model import Base
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from models.user_model import User, Role
import os
import datetime
import jwt

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    admin_role = Role(name="Admin", description="Admin role")
    commercial_role = Role(name="Commercial", description="Commercial role")
    support_role = Role(name="Support", description="Support role")

    db.add_all([admin_role, commercial_role, support_role])
    db.commit()

    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_create_user(setup_database):
    db = setup_database
    auth_controller = AuthController(db)

    auth_controller.signup_user(
        employee_number=1,
        full_name="Test User",
        email="testuser@example.com",
        department="xxx",
        role_name="Commercial",
        password="password",
    )

    user = db.query(User).filter_by(email="testuser@example.com").first()
    assert user is not None
    assert user.full_name == "Test User"
    assert user.role.name == "Commercial"


def test_login_success(setup_database):
    db = setup_database
    auth_controller = AuthController(db)

    token = auth_controller.login_user("testuser@example.com", "password")
    assert token is not None


def test_login_failure(setup_database):
    db = setup_database
    auth_controller = AuthController(db)

    token = auth_controller.login_user("testuser@example.com", "wrongpassword")
    assert token is None


def test_token_expiration(setup_database):
    db = setup_database
    auth_controller = AuthController(db)

    token = auth_controller.login_user("testuser@example.com", "password")
    assert token is not None

    expired_token = jwt.encode(
        {"sub": "testuser@example.com", "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1)},
        "epic-events-secret-key",
        algorithm="HS256",
    )

    with open("token.txt", "w") as token_file:
        token_file.write(expired_token)

    assert not auth_controller.is_authenticated()


def test_permission_check(setup_database):
    db = setup_database
    auth_controller = AuthController(db)

    auth_controller.current_user = db.query(User).filter_by(email="testuser@example.com").first()

    assert auth_controller.get_user_permissions("testuser@example.com") == "Commercial"
