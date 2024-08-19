from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from controllers.auth_controller import AuthController
import config

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
