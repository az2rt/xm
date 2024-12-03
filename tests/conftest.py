import pytest
import random
import requests

from .utils.defaults import BASE_URL as URL


@pytest.fixture(autouse=False)
def create_list_of_orders():
    """
    Prepare 10 orders
    :return:
    """
    added_order = []
    for i in range(10):
        resp = requests.post(
            url=URL + "/orders",
            json={
                "stocks": "UERUSD",
                "quantity": random.randint(1, 100),
            }
        )
        if resp.status_code == 201:
            added_order.append(resp.json()['order_id'])
    return added_order

@pytest.fixture(autouse=False)
def create_order():
    """
    Create order
    :return: JSON
    """
    resp = requests.post(
        url=URL + "/orders",
        json={
            "stocks": "UERUSD",
            "quantity": random.randint(1, 100),
        }
    )
    if resp.status_code == 201:
        return resp.json()
    else:
        raise Exception(f"Failed to create order, server returns {resp.status_code}")

@pytest.fixture(autouse=False)
def create_and_delete_order(create_order):
    """
    Delete order before it become executed
    :param create_order:
    :return:
    """
    order = create_order
    resp = requests.delete(
        url=URL + f"/orders/{order['order_id']}"
    )
    if resp.status_code == 200:
        return order
    else:
        raise Exception(f"Failed to create order, server returns {resp.status_code}")
