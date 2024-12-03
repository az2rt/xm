import random
import uuid

import pytest
import time
import requests
from .utils.defaults import BASE_URL

class TestGetOrder:

    def test_positive_case(self, create_order):
        """
        Steps:
        1 - Create order
        2 - Check response code
        3 - Check response body type
        4 - Check status or order
        """
        order = create_order
        resp = requests.get(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )
        assert resp.status_code == 200, f"Wrong status code: {resp.status_code}"
        assert isinstance(resp.json(), dict), f"Expected dict, instead of {type(resp.json())}"
        assert resp.json()['status'] == 'pending', f"Wrong order status: {resp.json()['status']}"

    def test_create_order_wait_5_sec_check_status(self, create_order):
        """
        Сheck order status change after some time (in task doesn't say the exact time, I took 5 seconds as an example)
        Steps:
        1 - Create order
        2 - Wait 5 sec
        3 - Send request to get order
        4 - Check response code
        5 - Check response body type
        6 - Check status or order
        """
        order = create_order
        time.sleep(5)
        resp = requests.get(
            url=f"{BASE_URL}/orders/{order['order_id']}",
        )
        assert resp.status_code == 200, f"Wrong status code: {resp.status_code}"
        assert isinstance(resp.json(), dict), f"Expected dict, instead of {type(resp.json())}"
        assert resp.json()['status'] == 'executed', f"Wrong order status: {resp.json()['status']}"

    @pytest.mark.parametrize(
        'value, response',
        [
            ('1234', {"status_code": 404, "message": "Order not found"}),
            (str(uuid.uuid4()), {"status_code": 404, "message": "Order not found"}),
            (random.randint(0, 2**32), {"status_code": 404, "message": "Order not found"}),
            (' ', {"status_code": 404, "message": "Order not found"})
        ])
    def test_negative_case(self, value, response):
        """
        Check non-exist order with different value (validation)
        Steps:
        1 - Send request to get order with value '1234'/uuid4/random int/<space>
        2 - Check response code
        3 - Check response message
        """
        resp = requests.get(
            url=f"{BASE_URL}/orders/{value}",
        )

        assert resp.status_code == response['status_code'], f"Wrong status code: {resp.status_code}"
        assert resp.json()['message'] == response['message'], f"Wrong message: {resp.json()}"

