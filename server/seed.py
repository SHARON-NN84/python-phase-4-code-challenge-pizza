from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("🌱 Deleting old data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("🌱 Seeding restaurants...")
    r1 = Restaurant(name="Karen's Pizza Shack", address="123 Main St")
    r2 = Restaurant(name="Sanjay's Pizza", address="456 Broadway")
    r3 = Restaurant(name="Kiki's Pizza", address="789 Pizza Lane")

    db.session.add_all([r1, r2, r3])

    print("🌱 Seeding pizzas...")
    p1 = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    p2 = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    p3 = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")

    db.session.add_all([p1, p2, p3])

    print("🌱 Linking pizzas to restaurants (RestaurantPizza)...")
    rp1 = RestaurantPizza(price=10, restaurant=r1, pizza=p1)
    rp2 = RestaurantPizza(price=15, restaurant=r2, pizza=p2)
    rp3 = RestaurantPizza(price=8, restaurant=r3, pizza=p1)
    rp4 = RestaurantPizza(price=12, restaurant=r3, pizza=p3)

    db.session.add_all([rp1, rp2, rp3, rp4])
    db.session.commit()

    print("✅ Done seeding!")
