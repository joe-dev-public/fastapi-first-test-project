import logging
from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


# Get all items
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# Add a single item to the db
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-data
def create_item(db: Session, item: schemas.ItemCreate, release_id: int):
    # (1) Create an SQLAlchemy model instance with the new data I want to add
    # (db_item could also reasonably be called new_item or something?).

    # Note: rather than do "url=item.url, total_price=item.total_price"
    # below, I think the tutorial is indicating we can do item.model_dump()
    # instead. (Where, presumably, *all* of the properties defined on
    # ItemCreate are added.) This is a dict and ** is just Python syntax to
    # copy one dict into another (a bit like ...spreading in JS).
    db_item = models.Item(
        **item.model_dump, created_at=datetime.now(), release_id=release_id
    )

    # Add instance to db session:
    db.add(db_item)

    # Commit changes:
    db.commit()

    # Refresh instance (so it can get new data from db, e.g. id):
    db.refresh(db_item)

    return db_item


# Get a single release by its id
def get_release(db: Session, release_id: int):
    return db.query(models.Release).filter(models.Release.id == release_id).first()


# Get all releases
def get_releases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Release).offset(skip).limit(limit).all()


# Get release for a given title (assumes for now that only one release per
# exact same title can/should exist)
def get_release_by_title(db: Session, title: str):
    return db.query(models.Release).filter(models.Release.title == title).first()


# Get all releases for a given artist (exact string match)
def get_releases_by_artist(db: Session, artist: str, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Release)
        .filter(models.Release.artist == artist)
        .offset(skip)
        .limit(limit)
        # Don't know if this .all is really necessary?
        .all()
    )


# Add a single release to the db
def create_release(db: Session, release: schemas.ReleaseCreate):
    # This is a verbose version of what we did with model_dump above;
    # listing each field manually:
    db_release = models.Release(
        created_at=datetime.now(), artist=release.artist, title=release.title
    )

    db.add(db_release)
    db.commit()
    db.refresh(db_release)
    return db_release
