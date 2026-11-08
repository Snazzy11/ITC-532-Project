
### 1
$ sh -c cd\ compose\ \&\&\ docker\ compose\ ps\ --format\ \"table\ \{\{.Service\}\}\\t\{\{.Status\}\}\"
SERVICE      STATUS
api          Up 2 minutes (healthy)
cache        Up 2 minutes (healthy)
db           Up 2 minutes (healthy)
directory    Up 2 minutes (healthy)
events       Up 2 minutes (healthy)
membership   Up 2 minutes (healthy)
proxy        Up About a minute (healthy)

[exit 0]

### 1
$ curl -fsS -i -w \\n -X POST http://localhost:8080/orders -H content-type:\ application/json -d \{\"club_id\":1\,\"student_name\":\"Test\ Student\"\,\"student_email\":\"student@example.edu\"\}
HTTP/1.1 201 Created
Server: nginx/1.31.6
Date: Sun, 08 Nov 2026 19:36:21 GMT
Content-Type: application/json
Content-Length: 81
Connection: keep-alive

{"club_id":1,"student_name":"Test Student","student_email":"student@example.edu"}

[exit 0]

### 2
$ curl -fsS -i -w \\n -X POST http://localhost:8080/users -H content-type:\ application/json -d \{\"name\":\"Ada\ Lovelace\"\,\"email\":\"ada@example.edu\"\}
HTTP/1.1 201 Created
Server: nginx/1.31.6
Date: Sun, 08 Nov 2026 19:38:02 GMT
Content-Type: application/json
Content-Length: 56
Connection: keep-alive

{"id":1,"name":"Ada Lovelace","email":"ada@example.edu"}

[exit 0]

### 2
$ sh -c cd\ compose\ \&\&\ docker\ compose\ down
 Container itc532-project-events-1 Stopping 
 Container itc532-project-proxy-1 Stopping 
 Container itc532-project-directory-1 Stopping 
 Container itc532-project-membership-1 Stopping 
 Container itc532-project-proxy-1 Stopped 
 Container itc532-project-proxy-1 Removing 
 Container itc532-project-proxy-1 Removed 
 Container itc532-project-api-1 Stopping 
 Container itc532-project-directory-1 Stopped 
 Container itc532-project-directory-1 Removing 
 Container itc532-project-directory-1 Removed 
 Container itc532-project-membership-1 Stopped 
 Container itc532-project-membership-1 Removing 
 Container itc532-project-membership-1 Removed 
 Container itc532-project-events-1 Stopped 
 Container itc532-project-events-1 Removing 
 Container itc532-project-events-1 Removed 
 Container itc532-project-api-1 Stopped 
 Container itc532-project-api-1 Removing 
 Container itc532-project-api-1 Removed 
 Container itc532-project-cache-1 Stopping 
 Container itc532-project-db-1 Stopping 
 Container itc532-project-db-1 Stopped 
 Container itc532-project-db-1 Removing 
 Container itc532-project-db-1 Removed 
 Container itc532-project-cache-1 Stopped 
 Container itc532-project-cache-1 Removing 
 Container itc532-project-cache-1 Removed 
 Network itc532-project_backend Removing 
 Network itc532-project_edge Removing 
 Network itc532-project_edge Removed 
 Network itc532-project_backend Removed 

[exit 0]

### 2
$ sh -c cd\ compose\ \&\&\ docker\ compose\ ps\ -a
NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS

[exit 0]

### 2
$ docker volume ls --filter name=itc532-project
DRIVER    VOLUME NAME
local     itc532-project_pgdata
local     itc532-project_valkeydata

[exit 0]

### 2
$ sh -c cd\ compose\ \&\&\ docker\ compose\ up\ -d\ --wait\ --wait-timeout\ 120
 Network itc532-project_backend Creating 
 Network itc532-project_backend Created 
 Network itc532-project_edge Creating 
 Network itc532-project_edge Created 
 Container itc532-project-cache-1 Creating 
 Container itc532-project-directory-1 Creating 
 Container itc532-project-events-1 Creating 
 Container itc532-project-db-1 Creating 
 Container itc532-project-membership-1 Creating 
 Container itc532-project-events-1 Created 
 Container itc532-project-membership-1 Created 
 Container itc532-project-directory-1 Created 
 Container itc532-project-cache-1 Created 
 Container itc532-project-db-1 Created 
 Container itc532-project-api-1 Creating 
 Container itc532-project-api-1 Created 
 Container itc532-project-proxy-1 Creating 
 Container itc532-project-proxy-1 Created 
 Container itc532-project-events-1 Starting 
 Container itc532-project-db-1 Starting 
 Container itc532-project-cache-1 Starting 
 Container itc532-project-membership-1 Starting 
 Container itc532-project-directory-1 Starting 
 Container itc532-project-db-1 Started 
 Container itc532-project-cache-1 Started 
 Container itc532-project-db-1 Waiting 
 Container itc532-project-cache-1 Waiting 
 Container itc532-project-events-1 Started 
 Container itc532-project-membership-1 Started 
 Container itc532-project-directory-1 Started 
 Container itc532-project-db-1 Healthy 
 Container itc532-project-cache-1 Healthy 
 Container itc532-project-api-1 Starting 
 Container itc532-project-api-1 Started 
 Container itc532-project-proxy-1 Starting 
 Container itc532-project-proxy-1 Started 
 Container itc532-project-proxy-1 Waiting 
 Container itc532-project-directory-1 Waiting 
 Container itc532-project-membership-1 Waiting 
 Container itc532-project-events-1 Waiting 
 Container itc532-project-api-1 Waiting 
 Container itc532-project-db-1 Waiting 
 Container itc532-project-cache-1 Waiting 
 Container itc532-project-db-1 Healthy 
 Container itc532-project-cache-1 Healthy 
 Container itc532-project-membership-1 Healthy 
 Container itc532-project-directory-1 Healthy 
 Container itc532-project-events-1 Healthy 
 Container itc532-project-api-1 Healthy 
 Container itc532-project-proxy-1 Healthy 

[exit 0]

### 2
$ curl -fsS -w \\n http://localhost:8080/users\?refresh=true
{"source":"database","served_by":"888b0ae76a2c:e9f209","users":[{"id":1,"name":"Ada Lovelace","email":"ada@example.edu"}]}

[exit 0]

### 3
$ sh -c cd\ compose\ \&\&\ docker\ compose\ ps\ --format\ \"table\ \{\{.Name\}\}\\t\{\{.Status\}\}\"
NAME                          STATUS
itc532-project-api-1          Up 48 seconds (healthy)
itc532-project-api-2          Up 47 seconds (healthy)
itc532-project-api-3          Up 47 seconds (healthy)
itc532-project-cache-1        Up 2 minutes (healthy)
itc532-project-db-1           Up 2 minutes (healthy)
itc532-project-directory-1    Up 48 seconds (healthy)
itc532-project-events-1       Up 48 seconds (healthy)
itc532-project-membership-1   Up 48 seconds (healthy)
itc532-project-proxy-1        Up 2 minutes (healthy)

[exit 0]

### 3
$ sh -ec for\ i\ in\ \$\(seq\ 1\ 12\)\;\ do\ curl\ -fsS\ http://localhost:8080/whoami\;\ done
67a59678adf2:5bd560
114c0ef889ec:d945ec
67a59678adf2:5bd560
114c0ef889ec:d945ec
67a59678adf2:5bd560
114c0ef889ec:d945ec
114c0ef889ec:d945ec
114c0ef889ec:d945ec
114c0ef889ec:d945ec
67a59678adf2:5bd560
114c0ef889ec:d945ec
d98229d21ed9:5df9eb

[exit 0]

### 3
$ sh -c cd\ compose\ \&\&\ docker\ compose\ logs\ --tail\ 12\ proxy
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.5:8000 status=200 upstream_status=200 time=0.004
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.003
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.5:8000 status=200 upstream_status=200 time=0.002
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.003
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.5:8000 status=200 upstream_status=200 time=0.002
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.002
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.5:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.8:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.22.0.7:8000 status=200 upstream_status=200 time=0.002

[exit 0]
