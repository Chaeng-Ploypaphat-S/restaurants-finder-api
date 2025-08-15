from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for Restaurant <-> MenuItem
restaurant_menuitem = db.Table('restaurant_menuitem',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True),
    db.Column('menuitem_id', db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
)

# Association table for Restaurant <-> PopularDish
restaurant_populardish = db.Table('restaurant_populardish',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True),
    db.Column('populardish_id', db.Integer, db.ForeignKey('popular_dish.id'), primary_key=True)
)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    website = db.Column(db.String(100))
    cuisine = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rating = db.Column(db.Float)
    menu_items = db.relationship('MenuItem', secondary=restaurant_menuitem, backref='restaurants')

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    
class PopularDish(db.Model):
    __tablename__ = 'popular_dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))