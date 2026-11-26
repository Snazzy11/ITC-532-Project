
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

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 9%/50%   2         6         2          66s

[exit 0]

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 140%/50%   2         6         6          3m20s

[exit 0]

### 2
$ sh -c date\;\ kubectl\ delete\ -f\ load-generator.yaml
Sun Nov 22 10:10:01 PM EST 2026
deployment.apps "load-generator" deleted from project namespace

[exit 0]

### 2
$ kubectl -n project get hpa
NAME         REFERENCE               TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 10%/50%   2         6         2          11m

[exit 0]

### 2
$ sh -c date\;\ kubectl\ -n\ project\ describe\ hpa\ membership\ \|\ tail\ -15
Sun Nov 22 10:18:23 PM EST 2026
Conditions:
  Type            Status  Reason               Message
  ----            ------  ------               -------
  AbleToScale     True    ScaleDownStabilized  recent recommendations were higher than current one, applying the highest recent recommendation
  ScaledToZero    False   NotScaledToZero      the HPA controller did not scale the workload to zero
  ScalingActive   True    ValidMetricFound     the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  False   DesiredWithinRange   the desired count is within the acceptable range
Events:
  Type    Reason             Age    From                       Message
  ----    ------             ----   ----                       -------
  Normal  SuccessfulRescale  11m    horizontal-pod-autoscaler  New size: 2; reason: Current number of replicas below Spec.MinReplicas
  Normal  SuccessfulRescale  10m    horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  10m    horizontal-pod-autoscaler  New size: 6; reason: cpu resource utilization (percentage of request) above target
  Normal  SuccessfulRescale  2m52s  horizontal-pod-autoscaler  New size: 5; reason: All metrics below target
  Normal  SuccessfulRescale  2m37s  horizontal-pod-autoscaler  New size: 2; reason: All metrics below target

[exit 0]

### 3
$ kubectl -n project wait --for=condition=complete job/membership-check --timeout=120s
job.batch/membership-check condition met

[exit 0]

### 3
$ kubectl -n project logs job/membership-check
membership-check passed

[exit 0]
