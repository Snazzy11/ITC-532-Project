
### 3
$ kubectl -n project wait --for=condition=complete job/membership-check --timeout=120s
job.batch/membership-check condition met

[exit 0]

### 3
$ kubectl -n project logs job/membership-check
membership-check passed

[exit 0]
