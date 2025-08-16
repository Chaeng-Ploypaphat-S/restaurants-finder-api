"""
Author: Ploypaphat (Chaeng) Saltz
File: routes.py
Description: Flask endpoints for Restaurant Finder API.
Created: August 2025
Copyright (c) Ploypaphat (Chaeng) Saltz. All rights reserved.
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants_finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, default=0.0)

# To support many-to-many relationship between menu items and restaurants
class RestaurantMenuItem(db.Model):
    __tablename__ = 'restaurant_menuitem'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    menuitem_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))

    restaurant = db.relationship('Restaurant', backref=db.backref('menuitem_links', cascade='all, delete-orphan'))
    menu_item = db.relationship('MenuItem', backref=db.backref('restaurant_links', cascade='all, delete-orphan'))
    
class PopularDish(db.Model):
    __tablename__ = 'popular_dish'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

# Many-to-many relationship between Restaurant and PopularDish
class RestaurantPopularDish(db.Model):
    __tablename__ = 'restaurant_populardish'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    populardish_id = db.Column(db.Integer, db.ForeignKey('popular_dish.id'))

    restaurant = db.relationship('Restaurant', backref=db.backref('populardish_links', cascade='all, delete-orphan'))
    popular_dish = db.relationship('PopularDish', backref=db.backref('restaurant_links', cascade='all, delete-orphan'))

with app.app_context():
    db.create_all()