import unittest
import time
from fastapi.testclient import TestClient

from fastapi_app.main import app
from shared.data import items

NUM_REQUESTS = 100  # Number of requests to make for each test


class TestPerformance(unittest.TestCase):
    """Basic performance benchmark tests for the FastAPI app."""

    @classmethod
    def setUpClass(cls):
        """Set up the test client."""
        cls.client = TestClient(app)
        print(f"\n--- Starting performance tests against FastAPI using TestClient ---")

    def setUp(self):
        """Resets the data before each test run for consistency."""
        items.clear()
        items.extend([
            {"id": 1, "name": "Laptop", "description": "A powerful laptop for development."},
            {"id": 2, "name": "Keyboard", "description": "A mechanical keyboard."},
            {"id": 3, "name": "Mouse", "description": "A wireless gaming mouse."},
        ])

    def test_get_all_items_performance(self):
        """Measures performance of the GET /items endpoint."""
        print(f"\nTesting GET /items ({NUM_REQUESTS} requests)")

        start_time = time.perf_counter()
        for _ in range(NUM_REQUESTS):
            response = self.client.get("/items")
            self.assertEqual(response.status_code, 200)
        end_time = time.perf_counter()

        total_time = end_time - start_time
        avg_time_ms = (total_time / NUM_REQUESTS) * 1000

        print(f"Total time: {total_time:.4f} seconds")
        print(f"Average time per request: {avg_time_ms:.4f} ms")
        self.assertTrue(True)

    def test_create_item_performance(self):
        """Measures performance of the POST /items endpoint."""
        items.clear()  # Start with a clean slate for this specific test
        print(f"\nTesting POST /items ({NUM_REQUESTS} requests)")

        start_time = time.perf_counter()
        for i in range(NUM_REQUESTS):
            item_data = {
                "name": f"PerfTest Item {i}",
                "description": "Item for performance test"
            }
            response = self.client.post("/items", json=item_data)
            self.assertEqual(response.status_code, 201)
        end_time = time.perf_counter()

        total_time = end_time - start_time
        avg_time_ms = (total_time / NUM_REQUESTS) * 1000

        print(f"Total time: {total_time:.4f} seconds")
        print(f"Average time per request: {avg_time_ms:.4f} ms")
        self.assertTrue(True)
