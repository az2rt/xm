from random import randint

import pytest
import requests

from .utils.tools import is_valid_uuid
from .utils.defaults import BASE_URL

class TestPostOrders:

    def test_create_order(self):
        """
        Check create order:
        Steps:
        1 - Create order
        2 - Check response code
        3 - Check response text
        4 - Check order id (expected uuid4 string)
        """
        resp = requests.post(
            url=f"{BASE_URL}/orders",
            json={
                "stocks": "EURUSD",
                "quantity": 1,
            }
        )
        assert resp.status_code == 201, f"Wrong status code: {resp.status_code}"
        assert resp.json()['message'] == "Order was created", f"Wrong message {resp.json()['message']}"
        assert is_valid_uuid(resp.json()['order_id']), f"Wrong UUID {resp.json()['order_id']}"

    @pytest.mark.parametrize(
        ('field', 'value', 'expected'),
        [
            ('stocks', [1, "", None], {'status_code': 400, 'message': 'Invalid input'}),
            ('quantity', ["123", "-10", "", "asd", None], {'status_code': 400, 'message': 'Invalid input'})
        ]
    )
    def test_validation_stocks_field(self, field, value, expected):
        """
        Check stocks field
        Steps:
        1 - try to create order with stocks=1/<empty string>/None
        2 - tru to create order with quantity=1/-10/<empty string>/asd/None

        """
        body={
            "stocks": None,
            "quantity": None
        }
        for i in value:
            if field == 'stocks':
                body[field] = i
                body['quantity'] = randint(0, 100)
            elif field == 'quantity':
                body[field] = i
                body['stocks'] = "EURUSD"

            resp = requests.post(
                url=f"{BASE_URL}/orders",
                json=body
            )

            assert resp.status_code == expected['status_code'], f"Wrong status code: {resp.status_code}"
            assert resp.json()['message'] == expected['message'], \
                f"Unxpected message {resp.json()['message']} for body {body}"

