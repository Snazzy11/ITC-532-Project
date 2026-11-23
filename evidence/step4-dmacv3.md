
### 1
$ kubectl run dnscheck -n project --rm -i --restart=Never --image=busybox:1.38.0 -- nslookup -type=a db-0.db-headless.project.svc.cluster.local.
Server:		10.43.0.10
Address:	10.43.0.10:53

Name:	db-0.db-headless.project.svc.cluster.local
Address: 10.42.0.131

All commands and output from this session will be recorded in container logs, including credentials and sensitive information passed through the command prompt.
If you don't see a command prompt, try pressing enter.
warning: couldn't attach to pod/dnscheck, falling back to streaming logs: unable to upgrade connection: container dnscheck not found in pod dnscheck_project
Server:		10.43.0.10
Address:	10.43.0.10:53

Name:	db-0.db-headless.project.svc.cluster.local
Address: 10.42.0.131

pod "dnscheck" deleted from project namespace

[exit 0]

### 1
$ kubectl -n project exec db-0 -- psql -U aXRjNTMy -d cG9zdGdyZXNxbDovL2l0YzUzMjpjaGFuZ2UtbWVAZGI6NTQzMi9pdGM1MzI -c CREATE\ TABLE\ IF\ NOT\ EXISTS\ survival\ \(note\ text\)\;\ INSERT\ INTO\ survival\ VALUES\ \(\'outlives\ the\ Pod\'\)\;
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  role "aXRjNTMy" does not exist
command terminated with exit code 2

[exit 2]

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
statefulset.apps/db   1/1     6m26s

NAME                                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/pgdata-db-0   Bound    pvc-20fa0e12-feb9-4e4e-8234-4a218bbee1df   500Mi      RWO            local-path     <unset>                 6m26s

NAME                                READY   STATUS    RESTARTS   AGE
pod/api-f4778d7fc-75tj4             1/1     Running   0          6m26s
pod/api-f4778d7fc-qszsk             1/1     Running   0          6m26s
pod/cache-d7bd8b557-fb5hn           1/1     Running   0          6m26s
pod/db-0                            1/1     Running   0          36s
pod/directory-7bf4845d4b-dlts6      1/1     Running   0          6m26s
pod/directory-7bf4845d4b-gc8qg      1/1     Running   0          6m26s
pod/firstservice-58fc8db456-gxfxx   1/1     Running   0          6m26s
pod/firstservice-58fc8db456-wx5ml   1/1     Running   0          6m26s
pod/membership-8586f4549-9cbx6      1/1     Running   0          6m26s
pod/membership-8586f4549-q2l95      1/1     Running   0          6m26s

[exit 0]

### 1
$ kubectl -n project exec db-0 -- psql -U itc532 -d itc532 -c SELECT\ note\ FROM\ survival\;
       note       
------------------
 outlives the Pod
(1 row)


[exit 0]

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 8%/50%   2         6         2          4m43s

[exit 0]

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 71%/50%   2         6         6          6m6s

[exit 0]

### 2
$ sh -c date\;\ kubectl\ delete\ -f\ load-generator.yaml
Sun Nov 22 17:40:46 EST 2026
deployment.apps "load-generator" deleted from project namespace

[exit 0]

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 7%/50%   2         6         2          12m

[exit 0]

### 2
$ sh -c date\;\ kubectl\ -n\ project\ describe\ hpa\ membership\ \|\ tail\ -15
Sun Nov 22 17:47:37 EST 2026
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooFewReplicas    the desired replica count is less than the minimum replica count
  ScaledToZero    False   NotScaledToZero   the HPA controller did not scale the workload to zero
Events:
  Type     Reason                        Age                From                       Message
  ----     ------                        ----               ----                       -------
  Warning  FailedGetResourceMetric       12m (x2 over 13m)  horizontal-pod-autoscaler  failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Warning  FailedComputeMetricsReplicas  12m (x2 over 13m)  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: unable to get metrics for resource cpu: no metrics returned from resource metrics API
  Normal   SuccessfulRescale             8m2s               horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             7m47s              horizontal-pod-autoscaler  New size: 6; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             77s                horizontal-pod-autoscaler  New size: 3; reason: All metrics below target
  Normal   SuccessfulRescale             62s                horizontal-pod-autoscaler  New size: 2; reason: All metrics below target

[exit 0]

### 3
$ kubectl -n project wait --for=condition=complete job/membership-check --timeout=120s
job.batch/membership-check condition met

[exit 0]

### 3
$ kubectl -n project logs job/membership-check
membership-check passed

[exit 0]
