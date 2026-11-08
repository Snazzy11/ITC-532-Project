import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_NAME = os.getenv("APP_NAME", "ITC 532 Module 1 Service")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(title=APP_NAME, version=APP_VERSION)


class Health(BaseModel):
    status: str
    timestamp: str
    hostname: str
    environment: str


class EchoRequest(BaseModel):
    message: str

class Order(BaseModel):
    order_id: int
    # 422 for orders
    item_name: str = Field(min_length=1)
    order_message: str = Field(min_length=1)

@app.get("/")
async def root():
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "hostname": socket.gethostname(),
        "docs": "/docs",
    }


@app.get("/health", response_model=Health)
async def health():
    return Health(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        hostname=socket.gethostname(),
        environment=ENVIRONMENT,
    )

@app.get("/compute/{n}")
def compute_factorial(n: int): # 422 for compute
    if n == 0:
        return 1
    return n * compute_factorial(n - 1)

@app.post("/orders")
async def create_order(payload: Order):
    return {"Ordered" : payload.item_name, 
            "Order Number" : payload.order_id, 
            "Requests" : payload.order_message}

@app.post("/echo")
async def echo(payload: EchoRequest):
    return {"you_sent": payload.message, "length": len(payload.message)}
