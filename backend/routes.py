from flask import jsonify, request

from backend.models import db, app, Restaurant, MenuItem, RestaurantMenuItem, PopularDish

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

# Restaurants Search API
@app.route('/restaurants', methods=['GET'])
def search_restaurants():
    cuisine = request.args.get('cuisine')
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    restaurants = Restaurant.query
    # Require at least one: cuisine or (latitude & longitude)
    if not cuisine and (latitude is None or longitude is None):
        return jsonify({"error": "At least one of 'cuisine' or both 'latitude' and 'longitude' is required."}), 400
    if cuisine:
        restaurants = restaurants.filter(Restaurant.cuisine.ilike(f'%{cuisine}%'))
    if latitude is not None and longitude is not None:
        lat_range = (latitude - 0.01, latitude + 0.01)
        lon_range = (longitude - 0.01, longitude + 0.01)
        restaurants = restaurants.filter(Restaurant.latitude.between(*lat_range), Restaurant.longitude.between(*lon_range))
    ids = [r.id for r in restaurants.all()]
    return jsonify({"restaurant_ids": ids})

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

# Menu & Popular Dishes API
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['GET'])
def restaurant_popular_dishes(restaurant_id):
    r = RestaurantMenuItem.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
    return jsonify({
        "restaurant_id": restaurant_id,
        "popular_dishes": []
    })
    
@app.route('/restaurant/<int:restaurant_id>/menu', methods=['POST'])
def add_restaurant_popular_dishes(restaurant_id):
    
    data = request.get_json(force=True)

    r = Restaurant.query.get(restaurant_id)
    if r is None:
        return jsonify({"error": f"Restaurant with id {restaurant_id} not found."}), 404
    
    m = MenuItem.query.filter_by(name=data['menu']).first()

    if m is None:
        menu_item = MenuItem(name=data['menu'])
        db.session.add(menu_item)
        db.session.commit()

    try:
        restaurant_menu_item = RestaurantMenuItem(restaurant_id=int(restaurant_id), menuitem_id=m.id if m else menu_item.id)
        db.session.add(restaurant_menu_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({
        "restaurant_id": restaurant_id,
        "popular_dishes": data['menu']
    })

if __name__ == '__main__':
    app.run(debug=True)
