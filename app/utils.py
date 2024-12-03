from starlette.middleware.base import BaseHTTPMiddleware
import random
import time


class DelayMiddleware(BaseHTTPMiddleware):
    """
    Generator of delay for every request
    """
    async def dispatch(self, request, call_next):
        delay = random.uniform(0.1, 1.0)
        time.sleep(delay)
        response = await call_next(request)
        return response