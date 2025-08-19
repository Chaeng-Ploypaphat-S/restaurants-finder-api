from src.routes import route_vendor

app = route_vendor.app

if __name__ == "__main__":
    app.run(debug=True)