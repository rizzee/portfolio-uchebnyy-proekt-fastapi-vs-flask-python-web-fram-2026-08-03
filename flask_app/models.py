from pydantic import BaseModel
from typing import Optional

# Pydantic model for creating an item.
# This helps validate the JSON body of POST requests.
class ItemCreate(BaseModel):
    name: str
    description: str

# Pydantic model for updating an item.
# This helps validate the JSON body of PUT/PATCH requests.
# Fields are optional for partial updates.
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
