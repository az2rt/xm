import asyncio
import datetime
import uuid

from fastapi import WebSocketDisconnect
from pydantic import BaseModel, field_validator, ValidationError
from typing import Dict, Literal, Optional


class OrderInput(BaseModel):
    """
    Class describe model of input Order
    """
    stocks: Optional[str]  # Currency pair symbol (e.g. 'EURUSD'), or any other stuff
    quantity: Optional[float]  # Quantity of the currency pair to be traded

    @field_validator('stocks')
    @classmethod
    def check_stocks(cls, v):
        if not isinstance(v, str) or v.strip() == "":
            raise ValueError("Stocks cannot be empty")
        return v

    @field_validator('quantity', mode='before')
    @classmethod
    def check_quantity(cls, v):
        if isinstance(v, str):
            raise ValueError("Quantity cannot be string")
        if not isinstance(v, (int, float)):
            raise ValueError("Quantity cannot be string")
        if  v is None or v <= 0:
            raise ValueError("Quantity cannot be empty")
        return v

class OrderOutput(BaseModel):
    """
    Class describe model of output Order
    """
    order_id: str | None = None  # Unique identifier for the order
    stocks: Optional[str]  # Currency pair symbol (e.g. 'EURUSD')
    quantity: Optional[float] = None  # Quantity of the currency pair to be traded
    status: Literal["pending", "executed", "canceled"] = "pending"  # Status of the order


class OrderManager:
    """
    Class to manage orders
    """
    def __init__(self):
        self._orders: Dict[str, OrderOutput] = dict()
        self._clients = []

    def get_clients(self):
        return self._clients

    def create_order(self, income_order: OrderInput):
        outcome_order = OrderOutput(
            order_id = str(uuid.uuid4()),
            stocks=income_order.stocks,
            quantity = income_order.quantity,
            status = "pending",
            datetime=datetime.datetime.now()
        )
        self._orders.update({outcome_order.order_id: outcome_order})

        asyncio.create_task(self.change_order_status(outcome_order.order_id))

        return outcome_order

    def get_all_orders(self):
        return [j for i, j in self._orders.items()]

    def get_order_by_id(self, order_id):
        return self._orders.get(order_id)

    def delete_order_by_id(self, order_id):
        try:
            self._orders[order_id].status = 'canceled'
            return True
        except KeyError:
            return False

    async def change_order_status(self, order):
        await asyncio.sleep(5)
        order = self.get_order_by_id(order)
        if order and order.status not in ("executed", "canceled"):
            order.status = "executed"
            for client in self._clients:
                try:
                    message = f"Order {order.order_id} has status {order.status}"
                    await client.send_text(message)
                except WebSocketDisconnect:
                    client.remove(client)


class ErrorException(BaseModel):
    """
    Base exception Class
    """

    code: int
    message: str

    def to_json(self):
        return self.dict()
