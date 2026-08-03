# shared/data.py

# This is a simple in-memory "database" for our items.
# It's a list of dictionaries that both the Flask and FastAPI apps will use.
# In a real-world application, you would use a proper database like PostgreSQL,
# MySQL, or a NoSQL database like MongoDB.

items = [
    {"id": 1, "name": "Laptop", "description": "A powerful laptop for development."},
    {"id": 2, "name": "Keyboard", "description": "A mechanical keyboard."},
    {"id": 3, "name": "Mouse", "description": "A wireless gaming mouse."},
]
