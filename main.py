from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, configure_mappers
from models.base_model import Base
from models.user_model import User, Role
from models.client_model import Client
from models.contract_model import Contract
from models.event_model import Event
from controllers.auth_controller import AuthController
import config

configure_mappers()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def main():
    db = SessionLocal()
    auth_controller = AuthController(db)

    auth_controller.start()


if __name__ == "__main__":
    init_db()
    main()
