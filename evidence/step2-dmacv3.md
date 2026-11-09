
### 1
$ sh -c cd\ compose\ \&\&\ docker\ compose\ ps\ --format\ \"table\ \{\{.Service\}\}\\t\{\{.Status\}\}\"
SERVICE      STATUS
api          Up 2 minutes (healthy)
cache        Up 5 minutes (healthy)
db           Up 5 minutes (healthy)
membership   Up 2 minutes (healthy)
proxy        Up 5 minutes (healthy)

[exit 0]

### 1
$ curl -s -w \\n http://localhost:8080/compute/10
{"n":10,"result":100}

[exit 0]

### 2
$ curl -s -w \\n -X POST http://localhost:8080/users -H content-type:\ application/json -d \{\"name\":\"Ada\ Lovelace\"\,\"email\":\"ada@example.edu\"\}
{"id":1,"name":"Ada Lovelace","email":"ada@example.edu"}

[exit 0]

### 2
$ sh -c cd\ compose\ \&\&\ docker\ compose\ down
 Container itc532-project-membership-1 Stopping 
 Container itc532-project-proxy-1 Stopping 
 Container itc532-project-proxy-1 Stopped 
 Container itc532-project-proxy-1 Removing 
 Container itc532-project-proxy-1 Removed 
 Container itc532-project-api-1 Stopping 
 Container itc532-project-membership-1 Stopped 
 Container itc532-project-membership-1 Removing 
 Container itc532-project-membership-1 Removed 
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
 Network itc532-project_backend Removed 
 Network itc532-project_edge Removed 

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
$ sh -c cd\ compose\ \&\&\ docker\ compose\ up\ -d\ --wait
 Network itc532-project_backend Creating 
 Network itc532-project_backend Created 
 Network itc532-project_edge Creating 
 Network itc532-project_edge Created 
 Container itc532-project-cache-1 Creating 
 Container itc532-project-db-1 Creating 
 Container itc532-project-membership-1 Creating 
 Container itc532-project-cache-1 Created 
 Container itc532-project-membership-1 Created 
 Container itc532-project-db-1 Created 
 Container itc532-project-api-1 Creating 
 Container itc532-project-api-1 Created 
 Container itc532-project-proxy-1 Creating 
 Container itc532-project-proxy-1 Created 
 Container itc532-project-cache-1 Starting 
 Container itc532-project-membership-1 Starting 
 Container itc532-project-db-1 Starting 
 Container itc532-project-db-1 Started 
 Container itc532-project-membership-1 Started 
 Container itc532-project-cache-1 Started 
 Container itc532-project-cache-1 Waiting 
 Container itc532-project-db-1 Waiting 
 Container itc532-project-db-1 Healthy 
 Container itc532-project-cache-1 Healthy 
 Container itc532-project-api-1 Starting 
 Container itc532-project-api-1 Started 
 Container itc532-project-proxy-1 Starting 
 Container itc532-project-proxy-1 Started 
 Container itc532-project-membership-1 Waiting 
 Container itc532-project-db-1 Waiting 
 Container itc532-project-cache-1 Waiting 
 Container itc532-project-proxy-1 Waiting 
 Container itc532-project-api-1 Waiting 
 Container itc532-project-db-1 Healthy 
 Container itc532-project-membership-1 Healthy 
 Container itc532-project-cache-1 Healthy 
 Container itc532-project-api-1 Healthy 
 Container itc532-project-proxy-1 Healthy 

[exit 0]

### 2
$ curl -s -w \\n http://localhost:8080/users\?refresh=true
{"source":"database","served_by":"46093d96ba0e:7d7ce1","users":[{"id":1,"name":"Ada Lovelace","email":"ada@example.edu"}]}

[exit 0]

### 3
$ sh -c cd\ compose\ \&\&\ docker\ compose\ ps\ --format\ \"table\ \{\{.Name\}\}\\t\{\{.Status\}\}\"
NAME                          STATUS
itc532-project-api-1          Up 33 seconds (healthy)
itc532-project-api-2          Up 33 seconds (healthy)
itc532-project-api-3          Up 33 seconds (healthy)
itc532-project-cache-1        Up 2 minutes (healthy)
itc532-project-db-1           Up 2 minutes (healthy)
itc532-project-membership-1   Up 34 seconds (healthy)
itc532-project-proxy-1        Up 2 minutes (healthy)

[exit 0]

### 3
$ sh -c for\ i\ in\ \$\(seq\ 1\ 12\)\;\ do\ curl\ -s\ http://localhost:8080/whoami\;\ done
e19658b1039c:34abcf
34d74d5659b8:a563ed
e19658b1039c:34abcf
34d74d5659b8:a563ed
9cd203e9b785:e4d64a
9cd203e9b785:e4d64a
e19658b1039c:34abcf
9cd203e9b785:e4d64a
e19658b1039c:34abcf
9cd203e9b785:e4d64a
34d74d5659b8:a563ed
e19658b1039c:34abcf

[exit 0]

### 3
$ sh -c cd\ compose\ \&\&\ docker\ compose\ logs\ --tail\ 12\ proxy
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.3:8000 status=200 upstream_status=200 time=0.002
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.5:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.3:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.5:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.6:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.6:8000 status=200 upstream_status=200 time=0.000
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.3:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.6:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.3:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.6:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.5:8000 status=200 upstream_status=200 time=0.001
proxy-1  | 192.168.143.2 "GET /whoami HTTP/1.1" -> 172.24.0.3:8000 status=200 upstream_status=200 time=0.001

[exit 0]
