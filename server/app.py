from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=("id", "name", "address")) for r in restaurants], 200
    
api.add_resource(Restaurants, "/restaurants")

class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(
                only=("id", "name", "address", "restaurant_pizzas")
            ), 200
        return {"error": "Restaurant not found"}, 404
    
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return "", 204
        else:
            return {"error": "Restaurant not found"}, 404
    
api.add_resource(RestaurantById, "/restaurants/<int:id>")

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict(only=("id", "name", "ingredients")) for p in pizzas], 200
    
api.add_resource(Pizzas, "/pizzas")

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id) 

        if not pizza or not restaurant:
            errors = []
            if not pizza:
                errors.append("Pizza not found")
            if not restaurant:
                errors.append("Restaurant not found")
            return {"errors": errors}, 404
        
        try:
            new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(new_rp)
            db.session.commit()
        except ValueError:
            return {"errors": ["validation errors"]}, 400
        
        return new_rp.to_dict(
            only=("id", "price", "pizza_id", "restaurant_id", "pizza", "restaurant")
        ), 201
    
api.add_resource(RestaurantPizzas, "/restaurant_pizzas")


if __name__ == "__main__":
    app.run(port=5555, debug=True)