from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .sql_app import crud, models, schemas
from .sql_app.database import SessionLocal, engine

# NB: if you want to reset the DB *every time the server reloads* (not
# necessarily very helpful!), then uncomment this line:
# models.Base.metadata.drop_all(bind=engine)
# More realistically, you can uncomment that line every time you change
# models.py, just for a quick way to recreate the relations from scratch.

# Basic approach to creating db tables:
models.Base.metadata.create_all(bind=engine)
# (Normally we'd use migrations, e.g. SQLAlchemy's tool "Alembic".)
# "will not attempt to recreate tables already present in the target database"
# https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all


# At first glance, it the above behaves like this:
# - Create the db in pg before starting the server.
# - Start the server. Relations get added to db as expected.
# - Modify models.py - relations unchanged regardless of restarting server.
# - Stop the server, drop and recreate the db.
# - Restart the server. Updated relations get added to the db as expected.
# So, not a brilliant workflow, but it is kinda temporary and fine for when
# we wanna change schema a lot and don't care about keeping data around.

app = FastAPI()

# Basic CORS stuff to enable local testing (maybe not the best approach)
my_origins = [
    "http://localhost:5173",
]

# Todo: can we remove CORS stuff if we're running in Docker?
app.add_middleware(
    CORSMiddleware,
    allow_origins=my_origins,
    # Yes, this is important! Otherwise only GET is allowed:
    allow_methods=["*"],
)


# Yield an independent db session/connection for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Todo: having skipped over stuff, don't know what response_model is yet,
# but can guess! Look into it to clarify.
@app.get("/items/", response_model=List[schemas.Item])
# Todo: I assume Depends is type annotated-related stuff? Look into this.
# Note: this is NOT asynchronous, which is potentially annoying? The FastAPI
# dev links to a deprecated tutorial about using "encode/databases" to connect
# to databases using async and await (https://fastapi.tiangolo.com/how-to/async-sql-encode-databases/).
# But ultimately, they seem to be saying "wait for SQLModel" (the kinda-ORM
# they're writing, based on SQLAlchemy, which maybe isn't that mature yet?).
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    if items == []:
        raise HTTPException(status_code=404, detail="No items found")
    return items


@app.get("/releases/{release_id}", response_model=schemas.Release)
def read_release(release_id: int, db: Session = Depends(get_db)):
    release = crud.get_release(db, release_id=release_id)
    if release is None:
        raise HTTPException(status_code=404, detail="Release not found")
    return release


# Todo: what's best practice here? We can't use two separate methods/path
# operators for "get all releases" and "get all releases with filter x".
# (Because order matters: whichever one comes first will handle all requests
# to that endpoint.)


# Get all releases (with optional filters)
# (Remember: the response model needs to be type List[] of the correct schema...)
@app.get("/releases/", response_model=List[schemas.Release])
def read_releases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    artist: Union[str, None] = None,
):
    # Todo: this is almost certainly *not* a good way to implement this :¬)
    # Keep an eye on tutorials for what's ~canonical~.
    if artist is not None:
        releases = crud.get_releases_by_artist(db, artist=artist)
        if releases == []:
            raise HTTPException(
                status_code=404, detail=f"No releases for artist '{artist}' found"
            )
    else:
        releases = crud.get_releases(db, skip=skip, limit=limit)
        if releases == []:
            raise HTTPException(status_code=404, detail="No releases found")
    return releases


@app.post("/releases/", response_model=schemas.Release)
def add_release(release: schemas.ReleaseCreate, db: Session = Depends(get_db)):
    db_release = crud.get_release_by_title(db, title=release.title)
    if db_release:
        raise HTTPException(
            status_code=400,
            detail=f"Release with title '{release.title}' already exists",
        )
    return crud.create_release(db=db, release=release)
