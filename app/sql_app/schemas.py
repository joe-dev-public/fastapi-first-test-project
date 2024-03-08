from datetime import datetime
from typing import List, Union

from pydantic import BaseModel

# Pydantic models != SQLAlchemy models
# For clarity, call Pydantic models "schema"


# Base schemas should have "common attributes [required for] creating or
# reading data" - this rings a bell from Rails.
# (https://fastapi.tiangolo.com/tutorial/sql-databases/#create-initial-pydantic-models-schemas)
class ItemBase(BaseModel):
    url: str
    # May use NUMERIC in Postgres, but in lieu of finding a better type to
    # use in Python, just convert to "pennies/cents/etc." somewhere :¬P
    total_price: Union[int, None] = None


class ItemCreate(ItemBase):
    pass


# Reading only: e.g. id isn't available when creating, but only after
# creation. Likewise, created_at.
class Item(ItemBase):
    id: int
    # Not sure if date is the right type to use here?
    created_at: datetime
    release_id: int

    # Seemingly just required to get Pydantic working with ORMs
    # (https://fastapi.tiangolo.com/tutorial/sql-databases/#use-pydantics-orm_mode)
    class Config:
        orm_mode = True


# Base: creating and reading
class ReleaseBase(BaseModel):
    artist: str
    title: str


# Creating only:
class ReleaseCreate(ReleaseBase):
    pass


# Reading only:
class Release(ReleaseBase):
    id: int
    created_at: datetime
    # To refer to the Item class here, this naturally needs to come after
    # it's defined
    items: List[Item] = []

    class Config:
        orm_mode = True
