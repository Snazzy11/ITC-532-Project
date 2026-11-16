
### 1
$ docker images project/api
IMAGE            ID             DISK USAGE   CONTENT SIZE   EXTRA
project/api:v1   9a8a17f90b18        286MB         66.9MB        

[exit 0]

### 1
$ docker images project/firstservice
IMAGE                     ID             DISK USAGE   CONTENT SIZE   EXTRA
project/firstservice:v1   f6ebce7f2b84        254MB         60.2MB        

[exit 0]

### 1
$ docker images project/directory
IMAGE                  ID             DISK USAGE   CONTENT SIZE   EXTRA
project/directory:v1   91f6f4b3d0a2        254MB         60.2MB        

[exit 0]

### 1
$ docker images project/membership
IMAGE                   ID             DISK USAGE   CONTENT SIZE   EXTRA
project/membership:v1   6da5df51155d        254MB         60.2MB        

[exit 0]

### 1
$ docker images project/api
IMAGE            ID             DISK USAGE   CONTENT SIZE   EXTRA
project/api:v1   bc359014d634        286MB         66.9MB        

[exit 0]

### 2
$ kubectl delete namespace project --ignore-not-found
namespace "project" deleted

[exit 0]

### 2
$ kubectl apply -f k8s/namespace.yaml
namespace/project created

[exit 0]

### 2
$ kubectl apply -R -f k8s/
configmap/api-config created
deployment.apps/api created
service/api created
deployment.apps/cache created
service/cache created
deployment.apps/db created
secret/db-credentials created
service/db created
deployment.apps/firstservice created
service/firstservice created
ingress.networking.k8s.io/project-ingress created
namespace/project unchanged

[exit 0]

### 2
$ kubectl -n project wait --for=condition=Available deploy --all --timeout=180s
deployment.apps/api condition met
deployment.apps/cache condition met
deployment.apps/db condition met
deployment.apps/firstservice condition met

[exit 0]

### 2
$ kubectl -n project get deploy\,svc\,ingress
NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/api            2/2     2            2           26s
deployment.apps/cache          1/1     1            1           26s
deployment.apps/db             1/1     1            1           26s
deployment.apps/firstservice   2/2     2            2           26s

NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/api            ClusterIP   10.43.51.138    <none>        8000/TCP   26s
service/cache          ClusterIP   10.43.165.218   <none>        6379/TCP   26s
service/db             ClusterIP   10.43.159.233   <none>        5432/TCP   26s
service/firstservice   ClusterIP   10.43.226.118   <none>        8000/TCP   26s

NAME                                        CLASS     HOSTS   ADDRESS         PORTS   AGE
ingress.networking.k8s.io/project-ingress   traefik   *       192.168.127.2   80      26s

[exit 0]

### 2
$ kubectl -n project get pods -o wide
NAME                            READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
api-f4778d7fc-6n9q2             1/1     Running   0          35s   10.42.0.61   macs-desktop   <none>           <none>
api-f4778d7fc-nvxfn             1/1     Running   0          35s   10.42.0.60   macs-desktop   <none>           <none>
cache-d7bd8b557-jr57b           1/1     Running   0          35s   10.42.0.59   macs-desktop   <none>           <none>
db-758dd7946-2tss2              1/1     Running   0          35s   10.42.0.62   macs-desktop   <none>           <none>
firstservice-5df867d647-kb6tb   1/1     Running   0          35s   10.42.0.64   macs-desktop   <none>           <none>
firstservice-5df867d647-pjw89   1/1     Running   0          35s   10.42.0.63   macs-desktop   <none>           <none>

[exit 0]

### 2
$ kubectl exec -n project curlbox -- curl -s http://api:8000/health
{"status":"healthy","instance":"api-f4778d7fc-nvxfn:0e64b6","checks":{"database":true,"cache":true}}
[exit 0]

### 2
$ sh -c kubectl\ -n\ project\ exec\ api-f4778d7fc-6n9q2\ --\ printenv\ \|\ sort\ \|\ grep\ -E\ \'ENVIRONMENT\|CACHE_TTL\|DATABASE\'
CACHE_TTL=30
DATABASE_URL=postgresql://itc532:change-me@db:5432/itc532
ENVIRONMENT=development

[exit 0]

### 2
$ kubectl -n project exec firstservice-5df867d647-kb6tb -- rm /tmp/ready

[exit 0]

### 2
$ kubectl -n project get endpointslices -l kubernetes.io/service-name=firstservice -o jsonpath=\{range\ .items\[\*\].endpoints\[\*\]\}\{.addresses\[0\]\}\{\"\\t\"\}\{.conditions.ready\}\{\"\\n\"\}\{end\}
10.42.0.64	false
10.42.0.63	true

[exit 0]

### 2
$ kubectl -n project get pod firstservice-5df867d647-kb6tb
NAME                            READY   STATUS    RESTARTS   AGE
firstservice-5df867d647-kb6tb   0/1     Running   0          6m29s

[exit 0]

### 2
$ kubectl -n project exec firstservice-5df867d647-kb6tb -- touch /tmp/ready

[exit 0]

### 3
$ kubectl apply -f k8s/firstservice/deployment.yaml
error: error parsing k8s/firstservice/deployment.yaml: error converting YAML to JSON: yaml: line 17: did not find expected key

[exit 1]

### 3
$ kubectl apply -f k8s/firstservice/deployment.yaml
deployment.apps/firstservice configured

[exit 0]

### 3
$ kubectl -n project rollout status deployment/firstservice
deployment "firstservice" successfully rolled out

[exit 0]

### 3
$ kubectl -n project rollout history deployment/firstservice
deployment.apps/firstservice 
REVISION  CHANGE-CAUSE
1         <none>
2         set RELEASE=2 in deployment.yaml


[exit 0]

### 3
$ kubectl -n project set image deployment/firstservice firstservice=project/firstservice:v9.99.99
deployment.apps/firstservice image updated

[exit 0]

### 3
$ kubectl -n project rollout status deployment/firstservice --timeout=60s
Waiting for deployment "firstservice" rollout to finish: 1 out of 2 new replicas have been updated...
error: timed out waiting for the condition

[exit 1]

### 3
$ kubectl -n project get pods -l app=firstservice
NAME                            READY   STATUS             RESTARTS   AGE
firstservice-58fc8db456-pbfff   1/1     Running            0          4m49s
firstservice-58fc8db456-snk5s   1/1     Running            0          4m45s
firstservice-6f68d55f4d-kkq27   0/1     ImagePullBackOff   0          2m25s

[exit 0]

### 3
$ kubectl -n project get deployment firstservice
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
firstservice   2/2     1            2           19m

[exit 0]

### 3
$ kubectl -n project rollout undo deployment/firstservice
Warning: resource deployments/firstservice was previously managed with 'kubectl apply'. Rolling back will not update the kubectl.kubernetes.io/last-applied-configuration annotation, which may cause unexpected behavior on future 'kubectl apply' operations. Consider using 'kubectl apply' with your previous configuration file instead.
deployment.apps/firstservice rolled back

[exit 0]

### 3
$ kubectl -n project rollout status deployment/firstservice
deployment "firstservice" successfully rolled out

[exit 0]

### 3
$ kubectl -n project rollout history deployment/firstservice
deployment.apps/firstservice 
REVISION  CHANGE-CAUSE
1         <none>
3         set image to missing tag v9.99.99
4         set RELEASE=2 in deployment.yaml


[exit 0]
