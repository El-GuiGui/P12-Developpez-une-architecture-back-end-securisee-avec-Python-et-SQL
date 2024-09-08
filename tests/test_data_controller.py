import pytest
from controllers.data_controller import DataController
from models.base_model import Base
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from models.user_model import User, Role


@pytest.fixture(scope="module")
def setup_database():
    db = SessionLocal()
    yield db
    db.close()


def test_create_client(setup_database):
    db = setup_database
    data_controller = DataController(db, None)

    user = db.query(User).filter_by(email="testuser@example.com").first()
    data_controller.auth_controller.current_user = user

    data_controller.create_client()
    client = db.query(Client).filter_by(email="newclient@example.com").first()

    assert client is not None
    assert client.commercial_contact == "Test User"


def test_update_contract(setup_database):
    db = setup_database
    data_controller = DataController(db, None)

    contract_id = 1
    data_controller.update_contract(contract_id)

    contract = db.query(Contract).filter_by(id=contract_id).first()
    assert contract.total_amount == 2000
