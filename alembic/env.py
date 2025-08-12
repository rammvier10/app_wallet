# from myapp.models import Base
from app.models import Base  # теперь доступен твой Base
import os
import sys
from dotenv import load_dotenv
from urllib.parse import quote_plus

from alembic import context

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_dotenv()




config = context.config


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


config.set_main_option("sqlalchemy.url", build_db_url())


target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    from sqlalchemy import engine_from_config, pool

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
