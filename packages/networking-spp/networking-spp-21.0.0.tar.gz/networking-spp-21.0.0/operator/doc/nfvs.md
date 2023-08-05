# nfvs
Nfvs are optional components of spp resource.
Nfvs are supported to add new nfv and delete old nfv.
Resources and patches are supported to update too.

## Setup dpdk ports in worker nodes
This example assumes that all worker nodes have set up physical ports using [dpdk][].

[dpdk]:https://doc.dpdk.org/spp/setup/getting_started.html#binding-network-ports-to-dpdk

## Definition of nfv
The following defines the three nfv.
each nfv has a unique name formatted with `nfv:<sec-id>`.


```yaml
  nfvs:
    - name: nfv:1
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,2"
        socket-mem: "1024"
      resources: ["vhost:1", "vhost:2"]
      patches:
        - src: "vhost:1"
          dst: "vhost:2"
    - name: nfv:2
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,3"
        socket-mem: "1024"
      resources: ["vhost:3", "vhost:4"]
      patches:
        - src: "vhost:3"
          dst: "vhost:4"
    - name: nfv:3
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,4"
        socket-mem: "1024"
      resources: ["vhost:5", "vhost:6"]
      patches:
        - src: "vhost:5"
          dst: "vhost:6"
```

## Update nfv
```image
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ Host +++++++++++++++++++++++++++++++++++++++++++++
+                                                                                                             +
+              -----Pod-----           -------Pod------                                                       +
------         |  spp-ctl  |           |  spp-primary |                                                       +
phy:0|         -------------           ----------------                                                       +
------                                                                                                        +
phy:1|         -----Pod-----                       ------Pod-------                      -----Pod------       +
------         |           |        vhost:3 -----> |              | -----> vhost:4       |            |       +
phy:2|         |           |                       |              |                      |            |       +
------         |   nfv:1   | -----> vhost:2        |   nfv: 2     |        vhost:5 ----> |   nfv: 3   |       +
+              |           |                       |              |                      |            |       +
+              |           | <----- vhost:1        |              |        vhost:6 <---- |            |       +
+              -------------                       ----------------                      --------------       +
+                                                                                                             +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```

In order to make this model, create below yaml file named nfv1.yaml

```yaml
apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: nfv1
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
    portmask: "0x07"     # needs three ports bound by dpdk
  nfvs:
    - name: nfv:1
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,2"
        socket-mem: "1024"
      resources: ["vhost:1", "vhost:2"]
      patches:
        - src: "vhost:1"
          dst: "vhost:2"
    - name: nfv:2
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,3"
        socket-mem: "1024"
      resources: ["vhost:3", "vhost:4"]
      patches:
        - src: "vhost:3"
          dst: "vhost:4"
    - name: nfv:3
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,4"
        socket-mem: "1024"
      resources: ["vhost:5", "vhost:6"]
      patches:
        - src: "vhost:5"
          dst: "vhost:6"
```
Apply nfv1.yaml

```bash
$ kubectl apply -f nfv1.yaml

```
## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME   CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP      AGE   STATUS
nfv1   1/1   1/1       3/3    0/0   0/0       0/0            k8sn3   10.102.118.135   59s   Nfvs ready ids:3,1,2
```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp nfv1
Name:         nfv1
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"nfv1","namespace":"default"},"spec":{"ctl":{"image":"sppc/spp...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-03T07:43:13Z
  Generation:          1
  Resource Version:    2923467
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/nfv1
  UID:                 8803801f-2398-4ebc-a7a0-f09ab3eadff3
Spec:
  Ctl:
    Image:  sppc/spp-ctl:18.04
    Name:   ctl
  Nfvs:
    Eal:
      Lcores:        1,2
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            nfv:1
    Patches:
      Dst:  vhost:2
      Src:  vhost:1
    Resources:
      vhost:1
      vhost:2
    Eal:
      Lcores:        1,3
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            nfv:2
    Patches:
      Dst:  vhost:4
      Src:  vhost:3
    Resources:
      vhost:3
      vhost:4
    Eal:
      Lcores:        1,4
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            nfv:3
    Patches:
      Dst:  vhost:6
      Src:  vhost:5
    Resources:
      vhost:5
      vhost:6
  Primary:
    Eal:
      Lcores:        1
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            primary
    Portmask:        0x07
Status:
  Apps:
    Pods:    <nil>
    Status:
  Ctl:
    Pods:
      Name:   nfv1-ctl-pod
      Phase:  Running
    Status:   1/1
  Events:
    Ctl is created
    Primary is created
    Nfv 1 is created
    Nfv 2 is created
    Nfv 3 is created
  Mirrors:
    Pods:
    Status:  0/0
  Nfvs:
    Pods:
      1:
        Name:   nfv1-nfv-1-pod
        Phase:  Running
        Response:
          Client - Id:  1
          Patches:
            Dst:  vhost:2
            Src:  vhost:1
          Ports:
            phy:0
            phy:1
            phy:2
            vhost:1
            vhost:2
          Status:  running
      2:
        Name:   nfv1-nfv-2-pod
        Phase:  Running
        Response:
          Client - Id:  2
          Patches:
            Dst:  vhost:4
            Src:  vhost:3
          Ports:
            phy:0
            phy:1
            phy:2
            vhost:3
            vhost:4
          Status:  running
      3:
        Name:   nfv1-nfv-3-pod
        Phase:  Running
        Response:
          Client - Id:  3
          Patches:
            Dst:  vhost:6
            Src:  vhost:5
          Ports:
            phy:0
            phy:1
            phy:2
            vhost:5
            vhost:6
          Status:  running
    Status:        3/3
  Node:            k8sn3
  Pcaps:
    Pods:
    Status:  0/0
  Primary:
    Pods:
      Name:       nfv1-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.102.118.135
  Status:         Nfvs ready ids:3,1,2
  Vfs:
    Pods:
    Status:  0/0
Events:      <none>

```

Get all pods and service of nfv1
```bash
$ kubectl get all -o wide
NAME                   READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
pod/nfv1-ctl-pod       1/1     Running   0          2m46s   10.244.3.73   k8sn3   <none>           <none>
pod/nfv1-nfv-1-pod     1/1     Running   0          2m22s   10.244.3.75   k8sn3   <none>           <none>
pod/nfv1-nfv-2-pod     1/1     Running   0          2m22s   10.244.3.76   k8sn3   <none>           <none>
pod/nfv1-nfv-3-pod     1/1     Running   0          2m22s   10.244.3.77   k8sn3   <none>           <none>
pod/nfv1-primary-pod   1/1     Running   0          2m33s   10.244.3.74   k8sn3   <none>           <none>

NAME                       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE     SELECTOR
service/nfv1-ctl-service   ClusterIP   10.102.118.135   <none>        5555/TCP,6666/TCP,7777/TCP   2m46s   nfv1=ctl
```

Show status of the nfvs
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.102.118.135
Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > status
- spp-ctl:
  - address: 10.102.118.135:7777
- primary:
  - status: running
- secondary:
  - processes:
    1: nfv:1
    2: nfv:2
    3: nfv:3
spp > nfv 1; status
- status: running
- lcore_ids:
  - master: 1
  - slave: 2
- ports:
  - phy:0
  - phy:1
  - phy:2
  - vhost:1 -> vhost:2
  - vhost:2
spp > nfv 2; status
- status: running
- lcore_ids:
  - master: 1
  - slave: 3
- ports:
  - phy:0
  - phy:1
  - phy:2
  - vhost:3 -> vhost:4
  - vhost:4
spp > nfv 3; status
- status: running
- lcore_ids:
  - master: 1
  - slave: 4
- ports:
  - phy:0
  - phy:1
  - phy:2
  - vhost:5 -> vhost:6
  - vhost:6
```


Edit nfv1.yaml file , replace resources and patches of nfv:1 like below.

```yaml
      resources: ["vhost:1", "vhost:2", "vhost:7", "vhost:8"]
      patches:
        - src: "vhost:1"
          dst: "vhost:2"
        - src: "vhost:7"
          dst: "vhost:8"
```

Apply nfv1.yaml again.

```bash
$ kubectl apply -f nfv1.yaml

```

Show status of the nfvs again.
Resources and patches are updated.
```bash
spp > nfv 1; status
- status: running
- lcore_ids:
  - master: 1
  - slave: 2
- ports:
  - phy:0
  - phy:1
  - phy:2
  - vhost:1 -> vhost:2
  - vhost:2
  - vhost:7 -> vhost:8
  - vhost:8
```
