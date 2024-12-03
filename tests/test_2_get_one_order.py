import random
import uuid

import pytest
import time
import requests
from .utils.defaults import BASE_URL

class TestGetOrder:

    def test_positive_case(self, create_order):
        """
        Create order, check after creation
        :return:
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
        According to requirements status should be changed after 5 sec to executed
        :return:
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
        Try to get non-existent order
        :return:
        """
        resp = requests.get(
            url=f"{BASE_URL}/orders/{value}",
        )

        assert resp.status_code == response['status_code'], f"Wrong status code: {resp.status_code}"
        assert resp.json()['message'] == response['message'], f"Wrong message: {resp.json()}"

