import pytest
import requests
from .utils.defaults import BASE_URL


class TestGetAllOrders:

    def test_order_empty_list(self):
        """
        Checks empty order list
        Steps:
        1 - Send request to get all orders
        2 - Check response code
        3 - Check type of response body
        4 - Check that response body is empty list
        """
        resp = requests.get(
            url=f'{BASE_URL}/orders'
        )
        assert resp.status_code == 200, f"Something goes wrong, statuts_code {resp.status_code}"
        assert isinstance(resp.json(), list), f"Server return wrong type of date, expected list, returns {resp.json()}"
        assert resp.json() == []

    def test_order_positive(self, create_list_of_orders):
        """
        Checks positive order list
        Steps:
        1 - Create several orders (10)
        2 - Send request to get all orders
        3 - Check response code
        4 - Check type of response body
        5 - Check that in len of body equal to 10
        """
        added_orders = create_list_of_orders
        resp = requests.get(
            url=f'{BASE_URL}/orders'
        )
        assert resp.status_code == 200, f"Something goes wrong, statuts_code {resp.status_code}"
        assert isinstance(resp.json(), list), f"Server return wrong type of date, expected list, returns {resp.json()}"
        assert len(added_orders) == len(resp.json()), \
            f"Amount of list in memory more or less than expected {len(added_orders)}"


