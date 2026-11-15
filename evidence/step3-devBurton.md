### 1
$ git rev-parse HEAD
143b27af3efd095861da43e2f6a9ceca7c2b3eb7

[exit 0]

### 1
$ kubectl config current-context
rancher-desktop

[exit 0]

### 1
$ docker images project/api
IMAGE            ID             DISK USAGE   CONTENT SIZE   EXTRA
project/api:v1   07158c34431e        286MB         66.9MB   U    

[exit 0]

### 1
$ docker images project/membership
IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
project/membership:v1   e796ba22f600        254MB         60.2MB        

[exit 0]

### 1
$ docker images project/directory
IMAGE                  ID             DISK USAGE   CONTENT SIZE   EXTRA
project/directory:v1   bb54eaf2085c        254MB         60.2MB        

[exit 0]

### 1
$ docker images project/firstservice
IMAGE                     ID             DISK USAGE   CONTENT SIZE   EXTRA
project/firstservice:v1   5dc4f826d41f        254MB         60.2MB   U    

[exit 0]

### 1
$ docker compose --env-file compose/.env.example -f compose/compose.yaml config --quiet

[exit 0]

### 1
$ kubectl apply --dry-run=server -R -f k8s/
configmap/api-config unchanged (server dry run)
deployment.apps/api unchanged (server dry run)
service/api unchanged (server dry run)
deployment.apps/cache unchanged (server dry run)
service/cache unchanged (server dry run)
deployment.apps/db unchanged (server dry run)
secret/db-credentials unchanged (server dry run)
service/db unchanged (server dry run)
deployment.apps/firstservice unchanged (server dry run)
service/firstservice unchanged (server dry run)
ingress.networking.k8s.io/project-ingress configured (server dry run)
deployment.apps/membership unchanged (server dry run)
service/membership unchanged (server dry run)
namespace/project unchanged (server dry run)

[exit 0]

### 1
$ kubectl apply -R -f k8s/
configmap/api-config unchanged
deployment.apps/api unchanged
service/api unchanged
deployment.apps/cache unchanged
service/cache unchanged
deployment.apps/db unchanged
secret/db-credentials unchanged
service/db unchanged
deployment.apps/firstservice unchanged
service/firstservice unchanged
ingress.networking.k8s.io/project-ingress configured
deployment.apps/membership unchanged
service/membership unchanged
namespace/project unchanged

[exit 0]

### 1
$ kubectl -n project rollout restart deployment/membership
deployment.apps/membership restarted

[exit 0]

### 1
$ kubectl -n project rollout status deployment/membership --timeout=180s
Waiting for deployment "membership" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "membership" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "membership" rollout to finish: 1 out of 2 new replicas have been updated...
Waiting for deployment "membership" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "membership" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "membership" rollout to finish: 1 old replicas are pending termination...
deployment "membership" successfully rolled out

[exit 0]

### 1
$ kubectl -n project wait --for=condition=Available deploy --all --timeout=180s
deployment.apps/api condition met
deployment.apps/cache condition met
deployment.apps/db condition met
deployment.apps/firstservice condition met
deployment.apps/membership condition met

[exit 0]

### 1
$ kubectl -n project wait --for=condition=Ready pods --all --timeout=180s
pod/api-f4778d7fc-229vz condition met
pod/api-f4778d7fc-cj9hm condition met
pod/cache-d7bd8b557-wvmbg condition met
pod/db-758dd7946-sjk4h condition met
pod/firstservice-58fc8db456-88n8r condition met
pod/firstservice-58fc8db456-j985x condition met
pod/membership-f5fb44d78-nv9lh condition met
pod/membership-f5fb44d78-qbf67 condition met

[exit 0]

### 1
$ kubectl -n project get deploy\,pods\,svc\,ingress
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/api            2/2     2            2           10m
deployment.apps/cache          1/1     1            1           10m
deployment.apps/db             1/1     1            1           10m
deployment.apps/firstservice   2/2     2            2           10m
deployment.apps/membership     2/2     2            2           130m

NAME                                READY   STATUS    RESTARTS   AGE
pod/api-f4778d7fc-229vz             1/1     Running   0          10m
pod/api-f4778d7fc-cj9hm             1/1     Running   0          10m
pod/cache-d7bd8b557-wvmbg           1/1     Running   0          10m
pod/db-758dd7946-sjk4h              1/1     Running   0          10m
pod/firstservice-58fc8db456-88n8r   1/1     Running   0          10m
pod/firstservice-58fc8db456-j985x   1/1     Running   0          10m
pod/membership-f5fb44d78-nv9lh      1/1     Running   0          12s
pod/membership-f5fb44d78-qbf67      1/1     Running   0          18s

NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/api            ClusterIP   10.43.21.62    <none>        8000/TCP   10m
service/cache          ClusterIP   10.43.151.32   <none>        6379/TCP   10m
service/db             ClusterIP   10.43.42.43    <none>        5432/TCP   10m
service/firstservice   ClusterIP   10.43.125.76   <none>        8000/TCP   10m
service/membership     ClusterIP   10.43.66.225   <none>        8000/TCP   130m

NAME                                        CLASS     HOSTS   ADDRESS         PORTS   AGE
ingress.networking.k8s.io/project-ingress   traefik   *       192.168.127.2   80      130m

[exit 0]

### 1
$ kubectl -n project exec deployment/membership -- python -c import\ json\,\ urllib.request\ as\ u\,\ urllib.error\ as\ e\;\ root=json.load\(u.urlopen\(\"http://membership:8000/\"\)\)\;\ assert\ root\[\"app\"\]\ ==\ \"Club\ Membership\ Service\"\;\ print\(\"Membership\ Service:\"\,\ root\)\;\ health=json.load\(u.urlopen\(\"http://membership:8000/health\"\)\)\;\ assert\ health\[\"status\"\]\ ==\ \"healthy\"\;\ print\(\"Membership\ health:\"\,\ health\)\;\ schema=json.load\(u.urlopen\(\"http://membership:8000/openapi.json\"\)\)\;\ assert\ \"/memberships\"\ in\ schema\[\"paths\"\]\ and\ \"/orders\"\ not\ in\ schema\[\"paths\"\]\;\ assert\ \"MembershipRequest\"\ in\ schema\[\"components\"\]\[\"schemas\"\]\ and\ \"Order\"\ not\ in\ schema\[\"components\"\]\[\"schemas\"\]\;\ print\(\"OpenAPI\ exposes\ /memberships\ and\ MembershipRequest\;\ no\ membership\ /orders\"\)\;\ api=json.load\(u.urlopen\(\"http://api:8000/health\"\)\)\;\ assert\ api\[\"checks\"\]\ ==\ \{\"database\":\ True\,\ \"cache\":\ True\}\;\ print\(\"Shared\ API\ health:\"\,\ api\)
Membership Service: {'app': 'Club Membership Service', 'version': '2.0.0', 'environment': 'development', 'hostname': 'membership-f5fb44d78-qbf67', 'docs': '/docs'}
Membership health: {'status': 'healthy', 'timestamp': '2026-11-15T21:48:15.018369+00:00', 'hostname': 'membership-f5fb44d78-qbf67', 'environment': 'development'}
OpenAPI exposes /memberships and MembershipRequest; no membership /orders
Shared API health: {'status': 'healthy', 'instance': 'api-f4778d7fc-229vz:815722', 'checks': {'database': True, 'cache': True}}

[exit 0]

### 1
$ python3 -c $'import json, urllib.request as u, urllib.error as e\nroot=json.load(u.urlopen("http://localhost/")); assert root["service"] == "api"; print("Ingress /:", root)\npayload={"club_id":532,"student_name":"Task One","student_email":"task1@example.test"}\nreq=u.Request("http://localhost/memberships", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}); r=u.urlopen(req); body=json.load(r); assert r.status == 201 and body == payload; print("Ingress /memberships:", r.status, body)\npayload["club_id"]=0\ntry:\n    u.urlopen(u.Request("http://localhost/memberships", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}))\n    raise AssertionError("Invalid club ID was accepted")\nexcept e.HTTPError as err:\n    assert err.code == 422; print("Invalid club ID rejected:", err.code)\nreq=u.Request("http://localhost/echo", data=json.dumps({"message":"shared base preserved"}).encode(), headers={"Content-Type":"application/json"}); body=json.load(u.urlopen(req)); assert body["you_sent"] == "shared base preserved"; print("Doug Ingress /echo:", body)'
Ingress /: {'service': 'api', 'version': '1.0.0', 'environment': 'development', 'instance': 'api-f4778d7fc-229vz:815722'}
Ingress /memberships: 201 {'club_id': 532, 'student_name': 'Task One', 'student_email': 'task1@example.test'}
Invalid club ID rejected: 422
Doug Ingress /echo: {'you_sent': 'shared base preserved', 'length': 21}

[exit 0]

### 1
$ docker network create itc532-membership-check-100192
f6c43aa7cbb1320590efe366bc1a42cb2224150b22a6321bdbb2bf00dc6a9878

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-100192-member --network itc532-membership-check-100192 --network-alias membership project/membership:v1
e072f9b24cc859128d6ceded871ee40eb6ee4433fe2592bebec0e3fd8ac30764

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-100192-directory --network itc532-membership-check-100192 --network-alias directory project/directory:v1
8fc3f8166a6c8d4bd12cba0ba3d2f70744769956db87e5b623ae8e5a6726d25f

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-100192-proxy --network itc532-membership-check-100192 --network-alias proxy -v /mnt/c/dev/ITC-532-Project-Membership-Task1/compose/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.31.6-alpine
ab179d36739e90c6fd5651e4e096594e4de43eb66b48b25bd6a7eb4337816ac8

[exit 0]

### 1
$ docker exec itc532-membership-check-100192-proxy nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

[exit 0]

### 1
$ docker exec itc532-membership-check-100192-member python -c $'import json, time, urllib.request as u, urllib.error as e\nfor host in ("membership", "directory"):\n    for attempt in range(30):\n        try:\n            u.urlopen("http://"+host+":8000/health"); break\n        except (e.URLError, TimeoutError):\n            if attempt == 29: raise\n            time.sleep(1)\npayload={"club_id":532,"student_name":"Route Check","student_email":"route@example.test"}\nfor path in ("/memberships", "/orders"):\n    req=u.Request("http://proxy"+path, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}); r=u.urlopen(req); body=json.load(r); assert r.status == 201 and body == payload; print("Compose nginx", path, r.status, body)\ntry:\n    u.urlopen(u.Request("http://membership:8000/orders", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}))\n    raise AssertionError("Old membership /orders still exists")\nexcept e.HTTPError as err:\n    assert err.code == 404; print("Membership /orders removed:", err.code)'
Compose nginx /memberships 201 {'club_id': 532, 'student_name': 'Route Check', 'student_email': 'route@example.test'}
Traceback (most recent call last):
  File "<string>", line 11, in <module>
    req=u.Request("http://proxy"+path, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}); r=u.urlopen(req); body=json.load(r); assert r.status == 201 and body == payload; print("Compose nginx", path, r.status, body)
                                                                                                                                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError

[exit 1]

### 1
$ docker network create itc532-membership-check-102465
d3c94016cc91433f6042e83482497bdc11117d1c157212fa0cd6a5e230d65fbb

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-102465-member --network itc532-membership-check-102465 --network-alias membership project/membership:v1
add61c7471319acbcd7a7e6b52fa43b43c73d30cf099458a8385bc4d7f5d8ad9

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-102465-directory --network itc532-membership-check-102465 --network-alias directory project/directory:v1
9c9c5deb0316f6f68726cd6ddef70c3df2c87edbff18b1a76e890338bd9f403b

[exit 0]

### 1
$ docker run -d --name itc532-membership-check-102465-proxy --network itc532-membership-check-102465 --network-alias proxy -v /mnt/c/dev/ITC-532-Project-Membership-Task1/compose/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro nginx:1.31.6-alpine
4975c369ef31c45b4f601510ca52a19de4adac2ac5f87ff6b4b0463a009b63eb

[exit 0]

### 1
$ docker exec itc532-membership-check-102465-proxy nginx -t
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

[exit 0]

### 1
$ docker exec itc532-membership-check-102465-member python -c $'import json, time, urllib.request as u, urllib.error as e\nfor host in ("membership", "directory"):\n    for attempt in range(30):\n        try:\n            u.urlopen("http://"+host+":8000/health"); break\n        except (e.URLError, TimeoutError):\n            if attempt == 29: raise\n            time.sleep(1)\npayload={"club_id":532,"student_name":"Route Check","student_email":"route@example.test"}\nfor path in ("/memberships", "/orders"):\n    req=u.Request("http://proxy"+path, data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}); r=u.urlopen(req); body=json.load(r); expected=payload if path == "/memberships" else {"status":"received", **payload}; assert r.status == 201 and body == expected; print("Compose nginx", path, r.status, body)\ntry:\n    u.urlopen(u.Request("http://membership:8000/orders", data=json.dumps(payload).encode(), headers={"Content-Type":"application/json"}))\n    raise AssertionError("Old membership /orders still exists")\nexcept e.HTTPError as err:\n    assert err.code == 404; print("Membership /orders removed:", err.code)'
Compose nginx /memberships 201 {'club_id': 532, 'student_name': 'Route Check', 'student_email': 'route@example.test'}
Compose nginx /orders 201 {'status': 'received', 'club_id': 532, 'student_name': 'Route Check', 'student_email': 'route@example.test'}
Membership /orders removed: 404

[exit 0]
