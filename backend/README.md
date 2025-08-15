
## 1. Restaurant Search API
GET /restaurants?query=pizza&location=47.6062,-122.3321&radius=5000&cuisine=italian

Parameters:
- query – keywords (e.g., "pizza", "ramen")
- location – lat/long for search center
- cuisine

## 2. Restaurant Details API
GET /restaurants/{id}

POST /restaurants

Parameters:
- Name, address, phone, website
- Hours of operation
- Menu
- Rating

## 3. Menu & Popular Dishes API
GET /restaurants/{id}/menu-item
GET /restaurants/{id}/popular-dishes

POST /menu-item

Parameters:
- name
- description
- price