import unittest
from src.models.vendor import db, app, Restaurant, MenuItem, RestaurantMenuItem, PopularDish, RestaurantPopularDish

class VendorModelTestCase(unittest.TestCase):
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

    def test_restaurant_creation(self):
        r = Restaurant(
            name="Test Restaurant",
            address="123 Test St",
            phone="555-1234",
            website="http://testaurant.com",
            cuisine="Italian",
            latitude=1.23,
            longitude=4.56,
            rating=4.5
        )
        self._extracted_from_test_restaurant_popular_dish_link_12(r)
        self.assertEqual(r.name, "Test Restaurant")

    def test_menu_item_creation(self):
        m = MenuItem(
            name="Pizza",
            description="Cheesy and delicious",
            price=9.99
        )
        self._extracted_from_test_restaurant_popular_dish_link_12(m)
        self.assertEqual(m.name, "Pizza")

    def test_restaurant_menu_item_link(self):
        r = Restaurant(name="Test Restaurant", address="123 Test St", phone="555-1234", website="http://testaurant.com", cuisine="Italian", latitude=1.23, longitude=4.56, rating=4.5)
        m = MenuItem(name="Pizza", description="Cheesy and delicious", price=9.99)
        self._extracted_from_test_restaurant_popular_dish_link_4(r, m)
        link = RestaurantMenuItem(restaurant=r, menu_item=m)
        self._extracted_from_test_restaurant_popular_dish_link_12(link)
        self.assertEqual(link.restaurant.name, "Test Restaurant")
        self.assertEqual(link.menu_item.name, "Pizza")

    def test_popular_dish_creation(self):
        d = PopularDish(name="Spaghetti")
        self._extracted_from_test_restaurant_popular_dish_link_12(d)
        self.assertEqual(d.name, "Spaghetti")

    def test_restaurant_popular_dish_link(self):
        r = Restaurant(name="Test Restaurant", address="123 Test St", phone="555-1234", website="http://testaurant.com", cuisine="Italian", latitude=1.23, longitude=4.56, rating=4.5)
        d = PopularDish(name="Spaghetti")
        self._extracted_from_test_restaurant_popular_dish_link_4(r, d)
        link = RestaurantPopularDish(restaurant=r, popular_dish=d)
        self._extracted_from_test_restaurant_popular_dish_link_12(link)
        self.assertEqual(link.restaurant.name, "Test Restaurant")
        self.assertEqual(link.popular_dish.name, "Spaghetti")

    # TODO Rename this here and in `test_restaurant_creation`, `test_menu_item_creation`, `test_restaurant_menu_item_link`, `test_popular_dish_creation` and `test_restaurant_popular_dish_link`
    def _extracted_from_test_restaurant_popular_dish_link_4(self, r, arg1):
        db.session.add(r)
        db.session.add(arg1)
        db.session.commit()

    # TODO Rename this here and in `test_restaurant_creation`, `test_menu_item_creation`, `test_restaurant_menu_item_link`, `test_popular_dish_creation` and `test_restaurant_popular_dish_link`
    def _extracted_from_test_restaurant_popular_dish_link_12(self, arg0):
        db.session.add(arg0)
        db.session.commit()
        self.assertIsNotNone(arg0.id)

if __name__ == "__main__":
    unittest.main()