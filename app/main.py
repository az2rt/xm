from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from models import OrderManager, OrderInput, ErrorException
from utils import DelayMiddleware

app = FastAPI()
order_manager = OrderManager()
app.add_middleware(DelayMiddleware)


@app.get("/orders")
def get_orders():
    """
    Retrieve all orders
    :return: OrderManager instance
    """
    return order_manager.get_all_orders()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={'message': 'Invalid input'},
    )

@app.post("/orders", status_code=201)
async def create_order(order: OrderInput):
    """
    Create a new order
    """
    created_order = order_manager.create_order(order)
    return JSONResponse(status_code=201, content={"message": "Order was created", "order_id": created_order.order_id})

@app.get("/orders/{orderid}")
async def get_order(orderid: str):
    """
    Retrieve a specific order
    :param orderid: str
    :return: JSONResponse
    """
    order = order_manager.get_order_by_id(orderid)
    if order is None:
        error = ErrorException(code=404, message="Order not found")
        return JSONResponse(status_code=error.code, content=error.to_json())
    return JSONResponse(status_code=200, content={"status": order.status})

@app.delete("/orders/{orderid}", status_code=400)
async def delete_order(orderid: str):
    """
    Cancel an order
    :param orderid: str uuid
    :return: JSONResponse
    """
    order = order_manager.get_order_by_id(orderid)
    if order is not None:
        if order.status == 'canceled':
            return JSONResponse(status_code=400,
                                content={"message": f"Order is already canceled."})

        if order.status != 'pending':
            return JSONResponse(status_code=400,
                                content={"message": f"Order cannot be canceled with status {order.status}"})


    was_succes = order_manager.delete_order_by_id(orderid)
    await notify_clients({"order_id": orderid, "new_status": was_succes})
    if was_succes:
        return JSONResponse(status_code=200, content={"message": "Order was deleted"})
    else:
        error = ErrorException(code=404, message="Order not found")
        return JSONResponse(status_code=error.code, content=error.to_json())


# WEBSOCKETS

@app.websocket('/ws')
async def read_ws(websocket: WebSocket):
    """
    Websocket connection for real-time order information
    """
    await websocket.accept()
    clients = order_manager.get_clients()
    clients.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message: {message}")
    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")

async def notify_clients(message: dict):
    """
    :param message: dict - message that will be sent to all clients
    """
    clients = order_manager.get_clients()
    for client in clients:
        try:
            await client.send_json(message)
        except WebSocketDisconnect:
            clients.remove(client)
