from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Basically following this to get started:
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-sqlalchemy-parts

# This should work if you're just running locally (and have postgres setup
# correctly :¬)
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://fastapi:password@localhost/fastapi_first_project"
# )

# This is required to connect to the "independent" (non-Docker Compose)
# postgres Docker.
SQLALCHEMY_DATABASE_URL = (
    "postgresql://fastapi:topsecret@postgres-server/fastapi_first_project"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
