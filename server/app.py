from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Pizza API</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "address": r.address
    } for r in restaurants]), 200

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    return jsonify(restaurant.to_dict()), 200

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    db.session.delete(restaurant)
    db.session.commit()

    return '', 204

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in pizzas]), 200

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get("price")
    pizza_id = data.get("pizza_id")
    restaurant_id = data.get("restaurant_id")

    if price is None or pizza_id is None or restaurant_id is None or not (1 <= price <= 30):
        return jsonify({"errors": ["validation errors"]}), 400

    try:
        new_rp = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )
        db.session.add(new_rp)
        db.session.commit()

        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)
        return jsonify({
            "id": new_rp.id,
            "pizza": {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            },
            "pizza_id": new_rp.pizza_id,
            "price": new_rp.price,
            "restaurant": {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            },
            "restaurant_id": new_rp.restaurant_id
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

def test_creates_restaurant_pizzas(self):
    '''creates one restaurant_pizzas using a pizza_id, restaurant_id, and price with a POST request to /restaurant_pizzas.'''

    with app.app_context():
        fake = Faker()
        pizza = Pizza(name=fake.name(), ingredients=fake.sentence())
        restaurant = Restaurant(name=fake.name(), address=fake.address())
        db.session.add(pizza)
        db.session.add(restaurant)
        db.session.commit()

        # delete if existing in case price differs
        restaurant_pizza = RestaurantPizza.query.filter_by(
            pizza_id=pizza.id, restaurant_id=restaurant.id).one_or_none()
        if restaurant_pizza:
            db.session.delete(restaurant_pizza)
            db.session.commit()

        response = app.test_client().post(
            '/restaurant_pizzas',
            json={
                "price": 3,
                "pizza_id": pizza.id,
                "restaurant_id": restaurant.id,
            }
        )

        assert response.status_code == 201
        assert response.content_type == 'application/json'
        response = response.json
        assert response['price'] == 3
        assert response['pizza_id'] == pizza.id

if __name__ == '__main__':
    app.run(port=5555, debug=True)
