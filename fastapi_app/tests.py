import unittest
from fastapi.testclient import TestClient

from .main import app
from .models import ItemCreate, ItemUpdate
from shared.data import items
from shared.schemas import Item


class TestFastAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        items.clear()
        items.extend([
            {"id": 1, "name": "Test", "description": "Test item"},
            {"id": 2, "name": "Another", "description": "Another item"}
        ])

    def test_get_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_item(self):
        response = self.client.get("/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test")

    def test_create_item(self):
        new_item = {"name": "New", "description": "New item"}
        response = self.client.post("/items/", json=new_item)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "New")

    def test_update_item(self):
        update_data = {"name": "Updated"}
        response = self.client.put("/items/1", json=update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Updated")

    def test_delete_item(self):
        response = self.client.delete("/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(items), 1)

    def test_not_found(self):
        response = self.client.get("/items/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()