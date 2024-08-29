from dotenv import load_dotenv
import os

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

DB_USER = os.getenv("DB_USER", "adm_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "adm6crm")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "crm_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
