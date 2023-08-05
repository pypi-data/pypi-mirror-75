# Usage
Here is an usage how to create, get, update and delete spp custom resource.

## Start spp operator
Before operating spp resource, you need to start spp operator in the master node.

Note that before starting spp operator, CRD must be defined in the cluster, otherwise spp operator start will be failure.

```bash
$ cd $GOPATH/src/opendev.org/x/networking-spp/operator
$ export OPERATOR_NAME=spp-operator
$ operator-sdk up local
```

## Create a new spp resource
Create a yaml file named spp1.yaml
```bash
$ vi spp1.yaml
```

Write the below to the file and save it.

Here, Spp is a kind of custom resources.
spp1 is the name to identify spp resource, ctl and primary are basic components.
Spp also has some optional components [nfvs](./doc/nfvs.md), [vfs](./doc/vfs.md), [mirrors](./doc/mirrors.md), [pcaps](./doc/pcaps.md), etc to make complex models.
```yaml
apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: spp1
spec:
  ctl:
    name: ctl
    image: sppc/spp-ctl:18.04
  primary:
    name: primary
    image: sppc/spp-ubuntu:18.04
    eal:
      lcores: "1"
      socket-mem: "1024"
      vdevs: [["net_tap1", "iface=foo1"]]
    portmask: "0x01"
```
Apply the file.
```bash
$ kubectl apply -f spp1.yaml
```

## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME           CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP      AGE   STATUS
spp1           1/1   1/1       0/0    0/0   0/0       0/0            k8sn1   10.104.231.178   55s   Primary is ready
```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp spp1
Name:         spp1
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"spp1","namespace":"default"},"spec":{"ctl":{"image":"sppc/spp...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-03T07:17:02Z
  Generation:          1
  Resource Version:    2919586
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/spp1
  UID:                 7fc7308a-73fd-4202-ab7f-f5a1bff4687c
Spec:
  Ctl:
    Image:  sppc/spp-ctl:18.04
    Name:   ctl
  Primary:
    Eal:
      Lcores:        1
      Socket - Mem:  1024
      Vdevs:
        [net_tap1 iface=foo1]
    Image:     sppc/spp-ubuntu:18.04
    Name:      primary
    Portmask:  0x01
Status:
  Apps:
    Pods:    <nil>
    Status:
  Ctl:
    Pods:
      Name:   spp1-ctl-pod
      Phase:  Running
    Status:   1/1
  Events:
    Ctl is created
    Primary is created
  Mirrors:
    Pods:
    Status:  0/0
  Nfvs:
    Pods:
    Status:  0/0
  Node:      k8sn1
  Pcaps:
    Pods:
    Status:  0/0
  Primary:
    Pods:
      Name:       spp1-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.104.231.178
  Status:         Primary is ready
  Vfs:
    Pods:
    Status:  0/0
Events:      <none>
```

Also get all resources which the cluster has.
```bash
$ kubectl get all -o wide
NAME                           READY   STATUS    RESTARTS   AGE     IP             NODE    NOMINATED NODE   READINESS GATES
pod/spp1-ctl-pod               1/1     Running   0          4m19s   10.244.1.116   k8sn1   <none>           <none>
pod/spp1-primary-pod           1/1     Running   0          4m5s    10.244.1.117   k8sn1   <none>           <none>

NAME                               TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE     SELECTOR
service/spp1-ctl-service           ClusterIP   10.104.231.178   <none>        5555/TCP,6666/TCP,7777/TCP   4m19s   spp1=ctl
```

## Access using spp CLI
Use the IP address of service/spp-ctl-service to bind spp1.
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.104.231.178
```

Show spp1 status
```text
spp > status;
- spp-ctl:
  - address: 10.104.231.178:7777
- primary:
  - status: running
- secondary:
  - processes:
```

## Update the spp resource
Once a spp resource has been created, user can edit yaml file to update it again.
Only [nfvs](./doc/nfvs.md) ,[vfs](./doc/vfs.md), [mirrors](./doc/mirrors.md) and [pcaps](./doc/pcaps.md) components are supported to this update method.
Spp operator reconciles update of components of spp resource automatically.

## Delete the spp resource
```bash
$ kubectl delete spp spp1
```
