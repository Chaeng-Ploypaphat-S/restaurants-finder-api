import unittest
from backend.models import app, db, Restaurant, MenuItem, RestaurantMenuItem

class ModelTestCase(unittest.TestCase):
	def setUp(self):
		self.app = app
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.drop_all()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_create_restaurant(self):
		r = Restaurant(name="Testaurant", address="123 Test St", phone="1234567890", website="http://test.com", cuisine="Test", latitude=1.23, longitude=4.56, rating=5.0)
		db.session.add(r)
		db.session.commit()
		self.assertIsNotNone(r.id)
		self.assertEqual(r.name, "Testaurant")

	def test_create_menu_item(self):
		m = MenuItem(name="Pizza", description="Cheesy", price=9.99)
		db.session.add(m)
		db.session.commit()
		self.assertIsNotNone(m.id)
		self.assertEqual(m.name, "Pizza")

	def test_create_restaurant_menu_item(self):
		r = Restaurant(name="Testaurant", address="123 Test St", phone="1234567890", website="http://test.com", cuisine="Test", latitude=1.23, longitude=4.56, rating=5.0)
		m = MenuItem(name="Pizza", description="Cheesy", price=9.99)
		db.session.add(r)
		db.session.add(m)
		db.session.commit()
		link = RestaurantMenuItem(restaurant=r, menu_item=m)
		db.session.add(link)
		db.session.commit()
		self.assertIsNotNone(link.id)
		self.assertEqual(link.restaurant.name, "Testaurant")
		self.assertEqual(link.menu_item.name, "Pizza")

if __name__ == "__main__":
	unittest.main()
