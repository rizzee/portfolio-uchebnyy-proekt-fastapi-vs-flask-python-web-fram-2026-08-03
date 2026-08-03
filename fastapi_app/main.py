from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from shared.data import items
from shared.schemas import Item

app = FastAPI()


class ItemCreate(BaseModel):
    name: str
    description: str


@app.get("/items", response_model=List[Item])
async def read_items():
    """Get all items."""
    return items


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Get item by ID."""
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    new_item = Item(id=len(items), **item.dict())
    items.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    """Update existing item."""
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = Item(id=item_id, **item.dict())
    items[item_id] = updated_item
    return updated_item


@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete item by ID."""
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    items.pop(item_id)