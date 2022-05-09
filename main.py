from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import get_from_json, user_to_dict, order_to_dict, offer_to_dict
from datetime import datetime


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)


class Offer(db.Model):
    __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.create_all()


def insert_data():
    with db.session.begin():
        users = get_from_json('Users.json')
        orders = get_from_json('orders.json')
        offers = get_from_json('offers.json')

        new_users = []
        for user in users:
            new_users.append(
                User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone']
            ))
            db.session.add_all(new_users)

        new_orders = []
        for order in orders:
            new_orders.append(
                Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m-%d-%Y'),
                end_date=datetime.strptime(order['end_date'], '%m-%d-%Y'),
                address=order['address'],
                price=order['price']
            ))
            db.session.add_all(new_orders)

        new_offers = []
        for offer in offers:
            new_offers.append(
                Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            ))
            db.session.add_all(new_offers)
        db.session.commit()


def main():
    insert_data()
    app.run()


@app.route("/users/", methods=['GET', 'POST'])
def users_get_and_post():
    if request.method == 'GET':
        result = []
        users = User.query.all()
        for user in users:
            result.append(user_to_dict(user))
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        user = User(
            id=data.get('id'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            age=data.get('age'),
            email=data.get('email'),
            role=data.get('role'),
            phone=data.get('phone')
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user_to_dict(user))


@app.route("/users/<int:uid>", methods=['GET', 'PUT', 'DELETE'])
def users_get_put_delete(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        return user_to_dict(user)

    elif request.method == 'PUT':
        data = request.json
        user = User.query.get(uid)

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        db.session.add(user)
        db.session.commit()
        db.session.close()
        return "User updated"

    elif request.method == 'DELETE':
        user = User.query.get(uid)
        db.session.delete(user)
        db.session.commit()
        return "User deleted"


@app.route("/orders/", methods=['GET', 'POST'])
def orders_get_and_post():
    if request.method == 'GET':
        result = []
        orders = Order.query.all()
        for order in orders:
            result.append(order_to_dict(order))
        return jsonify(result)
    elif request.method == 'POST':
        data = request.get_json()
        order = Order(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            start_date=datetime.strptime(data['start_date'], '%m-%d-%Y'),
            end_date=datetime.strptime(data['end_date'], '%m-%d-%Y'),
            address=data['address'],
            price=data['price'],
            customer_id=data['customer_id'],
            executor_id=data['executor_id']
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(order_to_dict(order))


@app.route("/orders/<int:orid>", methods=['GET', 'PUT', 'DELETE'])
def orders_get_put_delete(orid):
    if request.method == 'GET':
        order = Order.query.get(orid)
        return order_to_dict(order)

    elif request.method == 'PUT':
        data = request.json
        order = Order.query.get(orid)

        order.name = data['name']
        order.description = data['description']
        order.start_date = datetime.strptime(data['start_date'], '%m-%d-%Y')
        order.end_date = datetime.strptime(data['end_date'], '%m-%d-%Y')
        order.address = data['address']
        order.price = data['price']
        order.customer_id = data['customer_id']
        order.executor_id = data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return "Order updated"

    elif request.method == 'DELETE':
        order = User.query.get(orid)
        db.session.delete(order)
        db.session.commit()
        return "Order deleted"


@app.route("/offers/", methods=['GET', 'POST'])
def offers_get_and_post():
    if request.method == 'GET':
        result = []
        offers = Offer.query.all()
        for offer in offers:
            result.append(offer_to_dict(offer))
        return jsonify(result)
    elif request.method == 'POST':
        data = request.json
        offer = Offer(
            id=data.get('id'),
            order_id=data.get('order_id'),
            executor_id=data.get('executor_id')
        )
        db.session.add(offer)
        db.session.commit()
        return jsonify(offer_to_dict(offer))


@app.route("/offers/<int:ofid>", methods=['GET', 'PUT', 'DELETE'])
def offers_get_put_delete(ofid):
    if request.method == 'GET':
        offer = Offer.query.get(ofid)
        return offer_to_dict(offer)

    elif request.method == 'PUT':
        data = request.json
        offer = Offer.query.get(ofid)

        offer.order_id = data['order_id']
        offer.executor_id = data['executor_id']

        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return "Offer updated"

    elif request.method == 'DELETE':
        offer = Offer.query.get(ofid)
        db.session.delete(offer)
        db.session.commit()
        return "Offer deleted"


if __name__=="__main__":
    main()
