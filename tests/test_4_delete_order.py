import time
import random

import pytest
import requests
from .utils.defaults import BASE_URL

class TestDeleteOrder:

    def test_positive_case(self, create_order):
        """
        Try to delete order (change status to cancelled).
        According to requirement, only pending status can be changed.
        :param create_order:
        :return:
        """
        order = create_order
        resp = requests.delete(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )
        assert resp.status_code == 200, f"Can't delete order, server returns {resp.status_code}"
        assert resp.json()['message'] == "Order was deleted", "Wrong message from server"

        resp = requests.get(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )

        assert resp.status_code == 200, f"Can't delete order, server returns {resp.status_code}"
        assert resp.json()['status'] == "canceled", "Wrong status"

    def test_negative_case(self, create_order):
        """
        Try to change status if order has executed status
        """
        order = create_order
        time.sleep(5)
        resp_delete = requests.delete(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )
        assert resp_delete.status_code == 400, f"Server returned wrong status: {resp_delete.status_code}"

        resp_order = requests.get(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )
        assert resp_delete.json()['message'] == f"Order cannot be canceled with status {resp_order.json()['status']}", \
            "Wrong message from server"

    def test_delete_non_exist_order(self):
        """
        Try to delete non-exist order
        :return:
        """
        resp = requests.delete(
            url=f"{BASE_URL}/orders/{random.randint(1, 100000000)}",
        )

        assert resp.status_code == 404, f"Server returned wrong status: {resp.status_code}"
        assert resp.json()['message'] == f"Order not found", "Wrong message from server"

    def test_delete_already_deleted_order(self, create_and_delete_order):
        """
        Try to delete already deleted order
        :return:
        """
        order = create_and_delete_order
        resp = requests.delete(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )

        assert resp.status_code == 400, f"Server returned wrong status: {resp.status_code}."
        assert resp.json()['message'] == f"Order is already canceled.", "Wrong message from server."