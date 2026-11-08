import json
import os
import socket
import time
import uuid
from contextlib import asynccontextmanager

import psycopg
import valkey
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from psycopg.rows import dict_row
from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://itc532:itc532@db:5432/itc532")
VALKEY_URL = os.getenv("VALKEY_URL", "valkey://cache:6379/0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
CACHE_TTL = int(os.getenv("CACHE_TTL", "30"))

# Generated once per process, because a container hostname is not
# guaranteed to differ between replicas. /whoami returns it.
INSTANCE_ID = f"{socket.gethostname()}:{uuid.uuid4().hex[:6]}"

CACHE_KEY = "users:all"
HITS_KEY = "replica:hits"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""

cache = valkey.Valkey.from_url(VALKEY_URL, decode_responses=True)


def connect():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Compose waits for the database to report healthy, which is not the
    # same as ready for this application, so retry anyway.
    for _attempt in range(30):
        try:
            with connect() as conn:
                conn.execute(SCHEMA)
                conn.commit()
            print(f"schema ready after {_attempt + 1} attempt(s)", flush=True)
            break
        except Exception:
            time.sleep(1)
    else:
        raise RuntimeError("database never became reachable")
    yield


app = FastAPI(title="ITC 532 Module 2 API", version=APP_VERSION, lifespan=lifespan)


class UserIn(BaseModel):
    name: str
    email: str


@app.get("/")
def root():
    return {
        "service": "api",
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "instance": INSTANCE_ID,
    }


@app.get("/whoami", response_class=PlainTextResponse)
def whoami():
    cache.hincrby(HITS_KEY, INSTANCE_ID, 1)
    return INSTANCE_ID + "\n"


@app.get("/health")
def health():
    checks = {"database": False, "cache": False}
    try:
        with connect() as conn:
            conn.execute("SELECT 1")
        checks["database"] = True
    except Exception:
        pass
    try:
        checks["cache"] = bool(cache.ping())
    except Exception:
        pass

    body = {
        "status": "healthy" if all(checks.values()) else "unhealthy",
        "instance": INSTANCE_ID,
        "checks": checks,
    }
    if not all(checks.values()):
        raise HTTPException(status_code=503, detail=body)
    return body


@app.get("/users")
def list_users(refresh: bool = False):
    if not refresh:
        cached = cache.get(CACHE_KEY)
        if cached is not None:
            return {"source": "cache", "served_by": INSTANCE_ID,
                    "users": json.loads(cached)}

    with connect() as conn:
        rows = conn.execute(
            "SELECT id, name, email FROM users ORDER BY id"
        ).fetchall()

    cache.setex(CACHE_KEY, CACHE_TTL, json.dumps(rows))
    return {"source": "database", "served_by": INSTANCE_ID, "users": rows}


@app.post("/users", status_code=201)
def create_user(user: UserIn):
    try:
        with connect() as conn:
            row = conn.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s) "
                "RETURNING id, name, email",
                (user.name, user.email),
            ).fetchone()
            conn.commit()
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail="email already exists")

    cache.delete(CACHE_KEY)
    return row


@app.get("/stats")
def stats():
    return {"served_by": INSTANCE_ID, "hits_per_replica": cache.hgetall(HITS_KEY)}
