"""
Author: Ploypaphat (Chaeng) Saltz
File: routes.py
Description: Flask endpoints for Restaurant Finder API.
Created: August 2025
Copyright (c) Ploypaphat (Chaeng) Saltz. All rights reserved.
"""


from flask import jsonify, request

from src.models.vendor import db, app, Restaurant, MenuItem, RestaurantMenuItem, PopularDish, RestaurantPopularDish

# Add MenuItem API
@app.route('/menu-item', methods=['POST'])
def add_menu_item():
    data = request.get_json(force=True)
    required_fields = ['name', 'description', 'price']
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data['name'], str) or not data['name'].strip():
        return jsonify({"error": "'name' must be a non-empty string."}), 400
    
    price = float(data['price'])

    try:
        menu_item = MenuItem(
            name=data['name'],
            description=data['description'],
            price=price
        )
        db.session.add(menu_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({
        "id": menu_item.id,
        "name": menu_item.name,
        "description": menu_item.description,
        "price": menu_item.price
    }), 201
    
# Add PopularDish API
@app.route('/popular-dish', methods=['POST'])
def add_popular_dish():
    data = request.get_json()
    required_fields = ['name']
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data['name'], str) or not data['name'].strip():
        return jsonify({"error": "'name' must be a non-empty string."}), 400

    try:
        popular_dish = PopularDish(
            name=data['name']
        )
        db.session.add(popular_dish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({
        "id": popular_dish.id,
        "name": popular_dish.name
    }), 201

# List Restaurants By Cuisine API
@app.route('/restaurants', methods=['GET'])
def search_restaurants():
    cuisine = request.args.get('cuisine')
    restaurants = Restaurant.query
    if cuisine:
        restaurants = restaurants.filter(Restaurant.cuisine == cuisine)
    names = [r.name for r in restaurants.all()]
    return jsonify({"restaurants": names})

# Restaurant Create API
@app.route('/restaurant/', methods=['POST'])
def create_restaurant():
    data = request.get_json()
    required_fields = ['name', 'address', 'phone', 'cuisine', 'website', 'latitude', 'longitude']
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    restaurant = Restaurant(
        name=data['name'],
        address=data['address'],
        phone=data['phone'],
        cuisine=data['cuisine'],
        website=data['website'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "phone": restaurant.phone,
        "cuisine": restaurant.cuisine,
        "website": restaurant.website,
        "latitude": restaurant.latitude,
        "longitude": restaurant.longitude
    }), 201

# Restaurant Details API
@app.route('/restaurant/<int:restaurant_id>', methods=['GET'])
def restaurant_details(restaurant_id):
    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
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
 
@app.route('/restaurant/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
    try:
        db.session.delete(r)
        db.session.commit()
        return jsonify({"message": f"Restaurant with id {restaurant_id} deleted successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    
@app.route('/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404

    data = request.get_json()
    allowed_fields = ['name', 'address', 'phone', 'website', 'cuisine', 'latitude', 'longitude']
    updated = False

    for field in allowed_fields:
        if field in data:
            setattr(r, field, data[field])
            updated = True

    if not updated:
        return jsonify({"error": "No valid fields provided for update."}), 400

    try:
        db.session.commit()
        return jsonify({
            "id": r.id,
            "name": r.name,
            "address": r.address,
            "phone": r.phone,
            "website": r.website,
            "cuisine": r.cuisine,
            "latitude": r.latitude,
            "longitude": r.longitude
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/restaurant/<int:restaurant_id>/menu', methods=['POST'])
def add_restaurant_menu(restaurant_id):
    
    data = request.get_json(force=True)

    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
    
    m = MenuItem.query.filter_by(name=data['name']).first()

    if m is None:
        m = MenuItem(name=data['name'])
        db.session.add(m)
        db.session.commit()

    try:
        restaurant_menu_item = RestaurantMenuItem(restaurant_id=int(restaurant_id), menuitem_id=m.id)
        db.session.add(restaurant_menu_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: failed to create restaurant menu item {str(e)}"}), 500

    return jsonify({
        "restaurant_id": restaurant_id,
        "menu name": m.name
    })
    
@app.route('/restaurant/<int:restaurant_id>/popular', methods=['POST'])
def add_restaurant_popular_dish(restaurant_id):

    data = request.get_json(force=True)

    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
    
    p = PopularDish.query.filter_by(name=data['name']).first()

    if p is None:
        p = PopularDish(name=data['name'])
        db.session.add(p)
        db.session.commit()

    try:
        restaurant_popular_dish = RestaurantPopularDish(restaurant_id=int(restaurant_id), populardish_id=p.id)
        db.session.add(restaurant_popular_dish)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: failed to create restaurant popular dish {str(e)}"}), 500

    return jsonify({
        "restaurant_id": restaurant_id,
        "popular-dish name": p.name
    })
    

@app.route('/data-vendor', methods=['GET'])
def show_data_vendors():
    menu_items = MenuItem.query.all()
    menu_items_json = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
        }
        for item in menu_items
    ]
    menu_data = {"count": len(menu_items_json), "data": menu_items_json}

    popular_items = PopularDish.query.all()
    popular_dishes_json = [
        {
            "id": item.id,
            "name": item.name,
        }
        for item in popular_items
    ]
    popular_dishes_data = {"count": len(popular_dishes_json), "data": popular_dishes_json}

    restaurant_items = Restaurant.query.all()
    restaurant_json = [
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
        for r in restaurant_items
    ]
    restaurant_data = {"count": len(restaurant_json), "data": restaurant_json}
    
    restaurant_menu_items = RestaurantMenuItem.query.all()
    restaurant_menu_json = [
        {
            "id": item.id,
            "restaurant_id": item.restaurant_id,
            "menuitem_id": item.menuitem_id
        }
        for item in restaurant_menu_items
    ]
    restaurant_menu_data = {"count": len(restaurant_menu_json), "data": restaurant_menu_json}

    restaurant_popular_dishes = RestaurantPopularDish.query.all()
    restaurant_popular_json = [
        {
            "id": item.id,
            "restaurant_id": item.restaurant_id,
            "populardish_id": item.populardish_id
        }
        for item in restaurant_popular_dishes
    ]
    restaurant_popular_data = {"count": len(restaurant_popular_json), "data": restaurant_popular_json}

    return jsonify({
        "menu_items": menu_data,
        "popular_dishes": popular_dishes_data,
        "restaurants": restaurant_data,
        "restaurant_menu_items": restaurant_menu_data,
        "restaurant_popular_dishes": restaurant_popular_data
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
