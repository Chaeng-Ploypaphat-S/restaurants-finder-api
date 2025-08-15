
from flask import Flask, jsonify, request
import os

from models import db, Restaurant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Restaurant Search API
@app.route('/restaurants', methods=['GET'])
def search_restaurants():
    query = request.args.get('query', '')
    cuisine = request.args.get('cuisine', '')
    restaurants = Restaurant.query
    if query:
        restaurants = restaurants.filter(Restaurant.name.ilike(f'%{query}%'))
    if cuisine:
        restaurants = restaurants.filter(Restaurant.cuisine.ilike(f'%{cuisine}%'))
    results = [
        {
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "phone": r.phone,
            "website": r.website,
            "cuisine": r.cuisine,
            "latitude": r.latitude,
            "longitude": r.longitude
        }
        for r in restaurants.all()
    ]
    return jsonify({"restaurants": results})

# Restaurant Details API
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def restaurant_details(restaurant_id):
    r = Restaurant.query.get_or_404(restaurant_id)
    return jsonify({
        "id": r.id,
        "name": r.name,
        "address": r.address,
        "phone": r.phone,
        "website": r.website,
        "cuisine": r.cuisine,
        "latitude": r.latitude,
        "longitude": r.longitude
    })

# Reviews & Ratings API
@app.route('/restaurants/<int:restaurant_id>/reviews', methods=['GET'])
def restaurant_reviews(restaurant_id):
    return jsonify({
        "restaurant_id": restaurant_id,
        "reviews": []
    })

# Menu & Popular Dishes API
@app.route('/restaurants/<int:restaurant_id>/menu', methods=['GET'])
def restaurant_popular_dishes(restaurant_id):
    return jsonify({
        "restaurant_id": restaurant_id,
        "popular_dishes": []
    })


if __name__ == '__main__':
    app.run(debug=True)
