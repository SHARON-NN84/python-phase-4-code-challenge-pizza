from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant', cascade="all, delete")

    def to_dict(self, only=None):
        data = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }
        if only:
            return {k: v for k, v in data.items() if k in only}
        else:
            data['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]
            return data


class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def to_dict(self, only=None):
        data = {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }
        if only:
            return {k: v for k, v in data.items() if k in only}
        else:
            data['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]
            return data


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, value):
        if value < 1 or value > 30:
            raise ValueError("Price must be between 1 and 30")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'pizza': self.pizza.to_dict(only=('id', 'name', 'ingredients')),
            'restaurant': self.restaurant.to_dict(only=('id', 'name', 'address'))
        }
