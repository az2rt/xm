import argparse
import asyncio
import random
import time
import httpx
import websockets

from .utils.defaults import BASE_URL, WS_URL


async def create_order(client, index):
    body = {
        "stocks": f"STOCK-{index}",
        "quantity": random.randint(1, 100),
    }

    start_time = time.time()
    response = await client.post(
        f"{BASE_URL}/orders",
        json=body
    )
    end_time = time.time()

    if response.status_code == 201:
        order_id = response.json().get("order_id")
        return {"order_id": order_id, "start_time": start_time, "end_time": end_time}

async def receive_ws_messages(ws, expected_orders):
    """
    Checking ws and wait message Order <order_id> has status <status>
    And if status == executed, it means task complete
    """
    executed_orders = {}
    try:
        while len(executed_orders) < expected_orders:
            msg = await ws.recv()
            data = msg.split(' ')
            order_id = data[1]
            new_status = data[-1]
            if new_status == "executed":
                executed_orders[order_id] = time.time()

    except websockets.exceptions.ConnectionClosed:
        # just skip, if some reason connection closed before task complete
        pass
    return executed_orders

async def test_performance(order_count=100, batch_size=10):
    async with httpx.AsyncClient(timeout=30.0) as client, websockets.connect(WS_URL) as ws:
        order_results = []
        for i in range(0, order_count, batch_size):
            batch_tasks = [create_order(client, j) for j in range(i, min(i + batch_size, order_count))]
            order_results.extend(await asyncio.gather(*batch_tasks))
            # for some reason, timeout in httpx client doesn't work correctly
            # and I got time-to-time error httpx.ReadTimeout
            # I didn't find any other solution how to fix it istead of this sleep
            await asyncio.sleep(1)

        ws_task = asyncio.create_task(receive_ws_messages(ws, order_count))
        executed_orders = await ws_task

    delays = []
    for result in order_results:
        order_id = result["order_id"]
        if order_id and order_id in executed_orders:
            delay = executed_orders[order_id] - result["start_time"]
            delays.append(delay)

    avg_delay = sum(delays) / len(delays) if delays else 0

    print("Metrics:")
    print(f"Expected Orders: {order_count}")
    print(f"Executed Orders: {len(executed_orders)}")
    print(f"Delay (avarage): {avg_delay:.2f} seconds")
    print(f"Failed Orders: {order_count - len(delays)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", type=int, help="Count of order")
    parser.add_argument("-b", "--batch", type=int, help="Size of batch")
    args = parser.parse_args()
    asyncio.run(test_performance(args.count, args.batch))