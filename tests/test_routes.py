import unittest
import json
from backend.models import app, db

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


if __name__ == "__main__":
	unittest.main()
