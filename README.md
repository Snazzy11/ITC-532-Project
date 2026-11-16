# ITC 532 Project: Campus Club Directory

A microservices application run as one Docker Compose stack: an nginx reverse proxy,
a FastAPI `api` backed by PostgreSQL and Valkey, and one service per team member.

## Start the stack from a fresh clone

```bash
cp compose/.env.example compose/.env
# edit compose/.env and replace change-me with a real password
cd compose
docker compose up -d --build --wait
docker compose ps
curl -s http://localhost:8080/health
```

Run every `docker compose` command inside `compose/`, where Compose finds `.env`.

Scale the stateless `api` to three replicas:

```bash
cd compose
docker compose up -d --build --scale api=3 --wait
```

Stop the stack (named volumes, and the data in them, are kept):

```bash
cd compose
docker compose down
```

## Services and owners

| Service | Owner | Route through the proxy (port 8080) |
|---|---|---|
| `proxy` (nginx) | Parker Scott | `GET /healthz` |
| `api` (FastAPI) | Parker Scott | `/` and every path not listed below |
| `db` (PostgreSQL) | Parker Scott | not exposed, `backend` network only |
| `cache` (Valkey) | Parker Scott | not exposed, `backend` network only |
| `directory` | Parker Scott | `/compute/`, `/orders` |
| `membership` | devBurton | `POST /memberships` |
| `firstService` | dmacv3 | _added by owner_ |

## Membership requests

The membership service takes a club ID and the student's name and email at
`POST /memberships`.

To try it with Compose:

```bash
curl -i http://localhost:8080/memberships \
  -H 'Content-Type: application/json' \
  -d '{"club_id":532,"student_name":"Example Student","student_email":"student@example.test"}'
```

With Kubernetes, use `http://localhost/memberships` on port 80. Ingress sends
the request to the membership Service, which sends it to one of the two
membership Pods on port 8000.

Right now, it just checks the details and sends them back with a 201.