import pytest
from websockets import connect as ws_connect
from httpx import AsyncClient

from .utils.defaults import BASE_URL, WS_URL


@pytest.mark.asyncio
async def test_websocket_order_notifications():
    """
    Test WebSocket order notifications.
    Steps:
    1 - Make connection to websocket
    2 - Send request to create order
    3 - Check that message from server received
    """
    async with ws_connect(WS_URL) as websocket:
        # Create a new order
        async with AsyncClient(base_url=BASE_URL) as client:
            create_response = await client.post(
                "orders",
                json={"stocks": "EURUSD", "quantity": 10}
            )
            assert create_response.status_code == 201
            order_id = create_response.json()["order_id"]

        notification = await websocket.recv()
        assert order_id in notification
        assert "executed" in notification
