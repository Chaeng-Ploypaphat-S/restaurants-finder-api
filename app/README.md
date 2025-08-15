
## Restaurant Search API
GET /restaurants?query=pizza&location=47.6062,-122.3321&radius=5000&cuisine=italian

Parameters:
- query – keywords (e.g., "pizza", "ramen")
- location – lat/long for search center
- cuisine

## Restaurant Details API
GET /restaurants/{id}

Parameters:
- Name, address, phone, website
- Hours of operation
- Menu
- Rating

## Menu & Popular Dishes API
GET /restaurants/{id}/menu
GET /restaurants/{id}/popular-dishes