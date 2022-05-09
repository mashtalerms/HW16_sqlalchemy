import json


def get_from_json(path):
    with open(path, encoding='utf-8') as fp:
        result = json.load(fp)
        return result


def user_to_dict(user):
    return {
        'id':user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'age': user.age,
        'email': user.email,
        'role': user.role,
        'phone': user.phone
    }


def order_to_dict(order):
    return {
        'id':order.id,
        'name': order.name,
        'description': order.description,
        'start_date': order.start_date,
        'end_date': order.end_date,
        'address': order.address,
        'price': order.price
    }


def offer_to_dict(offer):
    return {
        'id':offer.id,
        'order_id': offer.order_id,
        'executor_id': offer.executor_id
    }
