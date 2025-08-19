import unittest
import json
from src.models.vendor import app, db, Restaurant, MenuItem, PopularDish, RestaurantMenuItem, RestaurantPopularDish

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_restaurant(self):
        data = {
            "name": "Testaurant",
            "address": "123 Test St",
            "phone": "1234567890",
            "website": "http://test.com",
            "cuisine": "Test",
            "latitude": 1.23,
            "longitude": 4.56
        }
        response = self.client.post("/restaurant/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_menu_item(self):
        data = {
            "name": "Pizza",
            "description": "Cheesy",
            "price": 9.99
        }
        response = self.client.post("/menu-item", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_popular_dish(self):
        data = {"name": "Spaghetti"}
        response = self.client.post("/popular-dish", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_search_restaurants(self):
        # Add a restaurant
        data = {
            "name": "Testaurant",
            "address": "123 Test St",
            "phone": "1234567890",
            "website": "http://test.com",
            "cuisine": "Italian",
            "latitude": 1.23,
            "longitude": 4.56
        }
        self.client.post("/restaurant/", data=json.dumps(data), content_type="application/json")
        # Search by cuisine
        response = self.client.get("/restaurants?cuisine=Italian")
        self.assertEqual(response.status_code, 200)
        self.assertIn("restaurants", response.get_json())

    def test_health_check(self):
        response = self.client.get("/health-check")
        self.assertEqual(response.status_code, 200)
        self.assertIn("menu_items", response.get_json())
        self.assertIn("popular_dishes", response.get_json())
        self.assertIn("restaurants", response.get_json())
        self.assertIn("restaurant_menu_items", response.get_json())
        self.assertIn("restaurant_popular_dishes", response.get_json())

if __name__ == "__main__":
    unittest.main()
