import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


def build_db_url() -> str:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")

    if not all([user, password, host, port, name]):
        raise ValueError("Missing database environment variables")

    password_encoded = quote_plus(password)
    return f"postgresql+psycopg2://{user}:{password_encoded}@{host}:{port}/{name}"


engine = create_engine(build_db_url(), pool_pre_ping=True, isolation_level="READ_COMMITTED")
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
