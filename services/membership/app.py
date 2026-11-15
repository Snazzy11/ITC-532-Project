import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import BaseModel, Field

APP_NAME = os.getenv("APP_NAME", "Club Membership Service")
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


class MembershipRequest(BaseModel):
    club_id: int = Field(gt=0)
    student_name: str = Field(min_length=2)
    student_email: str = Field(min_length=1)


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


@app.post("/echo")
async def echo(payload: EchoRequest):
    return {"you_sent": payload.message, "length": len(payload.message)}


@app.get("/compute/{n}")
async def compute(n: int):
    return {"n": n, "result": n * n}


@app.post("/memberships", status_code=201)
async def create_membership(payload: MembershipRequest):
    return payload.model_dump()
