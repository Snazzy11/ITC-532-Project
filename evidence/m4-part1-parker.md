
### 1
$ kubectl run dnscheck -n project --rm -i --restart=Never --image=busybox:1.38.0 -- nslookup -type=a db-0.db-headless.project.svc.cluster.local.
Server:		10.43.0.10
Address:	10.43.0.10:53

Name:	db-0.db-headless.project.svc.cluster.local
Address: 10.42.0.179

pod "dnscheck" deleted from project namespace

[exit 0]

### 1
$ kubectl -n project exec db-0 -- psql -U itc532 -d itc532 -c CREATE\ TABLE\ IF\ NOT\ EXISTS\ survival\ \(note\ text\)\;\ INSERT\ INTO\ survival\ VALUES\ \(\'outlives\ the\ Pod\'\)\;
CREATE TABLE
INSERT 0 1

[exit 0]

### 1
$ kubectl -n project delete pod db-0
pod "db-0" deleted from project namespace

[exit 0]

### 1
$ kubectl -n project get statefulset\,pvc\,pods
NAME                  READY   AGE
statefulset.apps/db   1/1     2m54s

NAME                                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/pgdata-db-0   Bound    pvc-fd14bd00-f5ec-48a8-9554-01c02739ccad   500Mi      RWO            local-path     <unset>                 2m54s

NAME                                READY   STATUS    RESTARTS      AGE
pod/api-f4778d7fc-8h9kn             1/1     Running   1 (89s ago)   2m54s
pod/api-f4778d7fc-lj2b8             1/1     Running   1 (88s ago)   2m54s
pod/cache-d7bd8b557-67jlq           1/1     Running   0             2m54s
pod/db-0                            1/1     Running   0             39s
pod/directory-7bf4845d4b-c7q45      1/1     Running   0             2m54s
pod/directory-7bf4845d4b-vkmc8      1/1     Running   0             2m54s
pod/firstservice-58fc8db456-444k4   1/1     Running   0             2m54s
pod/firstservice-58fc8db456-p78cx   1/1     Running   0             2m53s
pod/membership-8586f4549-fjld6      1/1     Running   0             2m53s
pod/membership-8586f4549-vd6wl      1/1     Running   0             2m53s

[exit 0]

### 1
$ kubectl -n project exec db-0 -- psql -U itc532 -d itc532 -c SELECT\ note\ FROM\ survival\;
       note       
------------------
 outlives the Pod
(1 row)


[exit 0]
