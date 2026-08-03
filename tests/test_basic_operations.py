import unittest
import requests
import os

# This file contains integration tests that run against a live server.
# It uses the `requests` library to make HTTP calls to the API endpoints.

# Read the base URL from an environment variable, with a default for FastAPI.
# To test Flask: API_BASE_URL='http://127.0.0.1:5000' pytest
BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:8000')

# A simple check to see if the server is running before attempting to run tests.
SERVER_IS_RUNNING = False
try:
    # Use a short timeout to avoid long waits if the server is down.
    # We check the /items endpoint as it's a primary part of the API.
    requests.get(f"{BASE_URL}/items", timeout=1)
    SERVER_IS_RUNNING = True
except requests.exceptions.RequestException:
    # If any request exception occurs, assume the server is not ready.
    pass


@unittest.skipIf(not SERVER_IS_RUNNING, f"API server not running or not responding at {BASE_URL}")
class TestBasicOperations(unittest.TestCase):
    """
    Test suite for core CRUD operations.
    These tests are designed to be run against a live server (either Flask or FastAPI).
    They are state-dependent and assume a clean slate at the beginning.
    """

    _shared_item = None

    @classmethod
    def setUpClass(cls):
        """
        Prepare the server state before running tests. This runs once.
        It cleans all items and creates one shared item for the tests to use.
        """
        # Clean up any existing items to ensure a predictable state.
        try:
            response = requests.get(f'{BASE_URL}/items')
            response.raise_for_status()
            for item in response.json():
                requests.delete(f'{BASE_URL}/items/{item["id"]}')
        except requests.RequestException as e:
            # If this fails, the server is likely in a bad state.
            raise RuntimeError(f"Failed to clean up items before test: {e}")

        # Add one item to be used by multiple tests
        item_payload = {"name": "Shared Test Item", "description": "An item for testing."}
        response = requests.post(f'{BASE_URL}/items', json=item_payload)
        if response.status_code != 201:
             raise RuntimeError(f"Failed to create initial item in setUpClass: {response.text}")
        cls._shared_item = response.json()

    @classmethod
    def tearDownClass(cls):
        """Clean up the shared item after all tests in the class have run."""
        if cls._shared_item:
            item_id = cls._shared_item['id']
            requests.delete(f'{BASE_URL}/items/{item_id}')

    def test_get_all_items(self):
        """Test GET /items - should contain exactly the one shared item."""
        response = requests.get(f'{BASE_URL}/items')
        self.assertEqual(response.status_code, 200)
        items = response.json()
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['id'], self._shared_item['id'])
        self.assertEqual(items[0]['name'], self._shared_item['name'])

    def test_get_single_item(self):
        """Test GET /items/{item_id} to retrieve the shared item."""
        item_id = self._shared_item['id']
        response = requests.get(f'{BASE_URL}/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], item_id)
        self.assertEqual(data['name'], self._shared_item['name'])

    def test_create_and_delete_item(self):
        """Test POST to create an item and then DELETE to remove it."""
        # 1. Create a new item
        new_item_payload = {"name": "Temporary Item", "description": "To be deleted."}
        post_response = requests.post(f'{BASE_URL}/items', json=new_item_payload)
        
        self.assertEqual(post_response.status_code, 201)
        created_item = post_response.json()
        item_id = created_item['id']
        self.assertEqual(created_item['name'], new_item_payload['name'])

        # 2. Verify it exists (list should now have 2 items)
        get_all_response = requests.get(f'{BASE_URL}/items')
        self.assertEqual(len(get_all_response.json()), 2)
        
        # 3. Delete the item
        delete_response = requests.delete(f'{BASE_URL}/items/{item_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json(), {"message": "Item deleted"})

        # 4. Verify it's gone (list should be back to 1 item)
        get_all_response_after = requests.get(f'{BASE_URL}/items')
        self.assertEqual(len(get_all_response_after.json()), 1)
        get_one_response = requests.get(f'{BASE_URL}/items/{item_id}')
        self.assertEqual(get_one_response.status_code, 404)

    def test_update_item(self):
        """Test PUT /items/{item_id} to update an item."""
        item_id = self._shared_item['id']
        original_name = self._shared_item['name']
        original_description = self._shared_item['description']

        update_payload = {"name": "Updated Name", "description": "Updated description."}
        
        # Update the item
        response = requests.put(f'{BASE_URL}/items/{item_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        updated_item = response.json()
        self.assertEqual(updated_item['name'], update_payload['name'])
        self.assertEqual(updated_item['description'], update_payload['description'])

        # Verify the update persisted
        get_response = requests.get(f'{BASE_URL}/items/{item_id}')
        self.assertEqual(get_response.json()['name'], update_payload['name'])
        
        # Revert the change to keep state consistent for other tests
        revert_payload = {"name": original_name, "description": original_description}
        revert_response = requests.put(f'{BASE_URL}/items/{item_id}', json=revert_payload)
        self.assertEqual(revert_response.status_code, 200)

    def test_nonexistent_item_endpoints(self):
        """Test GET, PUT, DELETE on a non-existent item ID."""
        bad_id = 99999
        
        # GET
        response_get = requests.get(f'{BASE_URL}/items/{bad_id}')
        self.assertEqual(response_get.status_code, 404)
        
        # PUT
        update_payload = {"name": "N/A", "description": "N/A"}
        response_put = requests.put(f'{BASE_URL}/items/{bad_id}', json=update_payload)
        self.assertEqual(response_put.status_code, 404)

        # DELETE
        response_delete = requests.delete(f'{BASE_URL}/items/{bad_id}')
        self.assertEqual(response_delete.status_code, 404)
