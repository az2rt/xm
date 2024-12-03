import os
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
WS_URL=os.getenv("WS_URL", "ws://127.0.0.1:8080/ws")