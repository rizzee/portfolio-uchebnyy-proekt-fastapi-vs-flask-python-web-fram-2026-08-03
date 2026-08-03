from pydantic import BaseModel

# This Pydantic model represents a single item in our data store.
# It's used for type hinting and response validation in FastAPI,
# and can be used for data validation in Flask as well.
# Sharing this schema ensures consistency between the two frameworks.
class Item(BaseModel):
    id: int
    name: str
    description: str
