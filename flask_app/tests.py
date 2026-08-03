import unittest
import json

from flask_app.main import app
from shared.data import items


class TestFlaskApp(unittest.TestCase):
    """Test suite for the Flask application."""

    def setUp(self):
        """Set up test client and initial data for each test."""
        # Create a test client for the Flask app
        self.client = app.test_client()
        # Enable testing mode to get better error messages
        app.testing = True

        # Reset the in-memory data store before each test to ensure isolation
        items.clear()
        items.extend([
            {"id": 1, "name": "Initial Item 1", "description": "First test item"},
            {"id": 2, "name": "Initial Item 2", "description": "Second test item"},
        ])

    def test_get_all_items(self):
        """Test retrieving all items."""
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Initial Item 1')

    def test_get_one_item(self):
        """Test retrieving a single item by its ID."""
        response = self.client.get('/items/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'Initial Item 1')

    def test_get_item_not_found(self):
        """Test retrieving a non-existent item."""
        response = self.client.get('/items/99')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Item not found')

    def test_create_item(self):
        """Test creating a new item."""
        new_item = {'name': 'New Item', 'description': 'A brand new item'}
        response = self.client.post(
            '/items',
            data=json.dumps(new_item),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # Check that the response contains the new item's data
        self.assertEqual(data['name'], 'New Item')
        self.assertEqual(data['description'], 'A brand new item')
        self.assertIn('id', data)
        # Check that the item was actually added to our data store
        self.assertEqual(len(items), 3)

    def test_create_item_invalid_data(self):
        """Test creating an item with invalid (missing) data."""
        invalid_item = {'description': 'This item is invalid because it has no name'}
        response = self.client.post(
            '/items',
            data=json.dumps(invalid_item),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_item(self):
        """Test updating an existing item."""
        updated_data = {'name': 'Updated Name', 'description': 'Updated Description'}
        response = self.client.put(
            '/items/1',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Updated Name')

        # Verify the item in the data store is actually updated
        updated_item_in_list = next((item for item in items if item['id'] == 1), None)
        self.assertIsNotNone(updated_item_in_list)
        self.assertEqual(updated_item_in_list['name'], 'Updated Name')

    def test_update_item_not_found(self):
        """Test updating a non-existent item."""
        updated_data = {'name': 'Updated Name'}
        response = self.client.put(
            '/items/99',
            data=json.dumps(updated_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_item(self):
        """Test deleting an existing item."""
        response = self.client.delete('/items/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Item deleted')

        # Verify the item is removed from the data store
        self.assertEqual(len(items), 1)
        item_ids = [item['id'] for item in items]
        self.assertNotIn(2, item_ids)

    def test_delete_item_not_found(self):
        """Test deleting a non-existent item."""
        response = self.client.delete('/items/99')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
