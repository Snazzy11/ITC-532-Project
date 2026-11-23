
### 1
$ kubectl run dnscheck -n project --rm -i --restart=Never --image=busybox:1.38.0 -- nslookup -type=a db-0.db-headless.project.svc.cluster.local.
Server:		10.43.0.10
Address:	10.43.0.10:53

Name:	db-0.db-headless.project.svc.cluster.local
Address: 10.42.0.148

pod "dnscheck" deleted from project namespace

[exit 0]

### 1
$ kubectl -n project exec db-0 -- sh -c exec\ psql\ -X\ -v\ ON_ERROR_STOP=1\ -U\ \"\$POSTGRES_USER\"\ -d\ \"\$POSTGRES_DB\"\ \"\$@\" psql -c CREATE\ TABLE\ IF\ NOT\ EXISTS\ survival\ \(note\ text\)\;\ INSERT\ INTO\ survival\ VALUES\ \(\'outlives\ the\ Pod\'\)\;
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
statefulset.apps/db   1/1     45s

NAME                                STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
persistentvolumeclaim/pgdata-db-0   Bound    pvc-ebe73863-cb26-4c02-ab15-f17a49c9506f   500Mi      RWO            local-path     <unset>                 45s

NAME                                READY   STATUS      RESTARTS      AGE
pod/api-f4778d7fc-gmpv2             1/1     Running     0             45s
pod/api-f4778d7fc-l2spm             1/1     Running     0             45s
pod/cache-d7bd8b557-qd2jj           1/1     Running     0             45s
pod/db-0                            1/1     Running     0             11s
pod/directory-7bf4845d4b-8zb8f      1/1     Running     0             45s
pod/directory-7bf4845d4b-rht6z      1/1     Running     0             45s
pod/firstservice-58fc8db456-jd462   1/1     Running     0             45s
pod/firstservice-58fc8db456-x49z8   1/1     Running     0             45s
pod/membership-8586f4549-85j8d      1/1     Running     0             45s
pod/membership-8586f4549-lh422      1/1     Running     0             45s
pod/membership-check-8fxdq          0/1     Completed   2 (40s ago)   45s

[exit 0]

### 1
$ kubectl -n project exec db-0 -- sh -c exec\ psql\ -X\ -v\ ON_ERROR_STOP=1\ -U\ \"\$POSTGRES_USER\"\ -d\ \"\$POSTGRES_DB\"\ \"\$@\" psql -c SELECT\ note\ FROM\ survival\;
       note
------------------
 outlives the Pod
(1 row)


[exit 0]

### 2
$ kubectl -n project get hpa membership
NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 8%/50%   2         6         2          50s

[exit 0]

### 2
$ kubectl -n project get hpa membership
NAME         REFERENCE               TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 176%/50%   2         6         6          2m

[exit 0]

### 2
$ sh -c date\;\ kubectl\ delete\ -f\ load-generator.yaml
Sun Nov 22 21:11:58 EST 2026
deployment.apps "load-generator" deleted from project namespace

[exit 0]

### 2
$ kubectl -n project get hpa membership
NAME         REFERENCE               TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
membership   Deployment/membership   cpu: 8%/50%   2         6         2          8m10s

[exit 0]

### 2
$ sh -c date\;\ kubectl\ -n\ project\ describe\ hpa\ membership\ \|\ tail\ -15
Sun Nov 22 21:18:08 EST 2026
  Type            Status  Reason            Message
  ----            ------  ------            -------
  AbleToScale     True    ReadyForNewScale  recommended size matches current size
  ScaledToZero    False   NotScaledToZero   the HPA controller did not scale the workload to zero
  ScalingActive   True    ValidMetricFound  the HPA was able to successfully calculate a replica count from cpu resource utilization (percentage of request)
  ScalingLimited  True    TooFewReplicas    the desired replica count is less than the minimum replica count
Events:
  Type     Reason                        Age    From                       Message
  ----     ------                        ----   ----                       -------
  Normal   SuccessfulRescale             8m11s  horizontal-pod-autoscaler  New size: 2; reason: Current number of replicas below Spec.MinReplicas
  Warning  FailedGetResourceMetric       7m56s  horizontal-pod-autoscaler  failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Warning  FailedComputeMetricsReplicas  7m56s  horizontal-pod-autoscaler  invalid metrics (1 invalid out of 1), first error is: failed to get cpu resource metric value: failed to get cpu utilization: did not receive metrics for targeted pods (pods might be unready)
  Normal   SuccessfulRescale             7m11s  horizontal-pod-autoscaler  New size: 4; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             6m56s  horizontal-pod-autoscaler  New size: 6; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             26s    horizontal-pod-autoscaler  New size: 2; reason: All metrics below target

[exit 0]

### 3
$ kubectl -n project wait --for=condition=complete job/membership-check --timeout=120s
job.batch/membership-check condition met

[exit 0]

### 3
$ kubectl -n project logs job/membership-check
membership-check passed

[exit 0]
