
## 1. Restaurant Search API
GET /restaurants?cuisine=italian

Parameters:
- cuisine

## 2. Restaurant Details API
GET /restaurant/{id}

POST /restaurant

Parameters:
- Name, address, phone, website
- Cuisine
- Latitude & longitude

## 3. Menu API
GET /restaurant/{id}/menu

POST /menu-item

Parameters:
- name
- description
- price

## 4. Popular Dish API
GET /restaurant/{id}/popular

POST /popular-dish

Parameters:
- name
