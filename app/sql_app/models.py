from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import relationship

from .database import Base

# Basically following this to get started (but using my own structure):
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    # modified_at = Column(Date)
    url = Column(String)
    total_price = Column(Numeric)
    release_id = Column(Integer, ForeignKey("releases.id"))

    release = relationship("Release", back_populates="items")


class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
    created_at = Column(TIMESTAMP)
    # modified_at = Column(Date)
    artist = Column(String)
    title = Column(String)

    items = relationship("Item", back_populates="release")
