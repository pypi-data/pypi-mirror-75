# pcaps
Pcaps are optional components of spp resource.
Pcaps are supported to add new pcap and delete old pcap.
Status component of pcap is supported to update too.

## Setup dpdk ports in worker nodes
This example assumes that all worker nodes have set up physical ports using [dpdk][].

[dpdk]:https://doc.dpdk.org/spp/setup/getting_started.html#binding-network-ports-to-dpdk

## Definition of pcap
The following defines two pcaps.
each pcap has a unique name formatted with `pcap:<sec-id>`.
the 1st is running pattern , 2nd pcap is idle pattern and mounts host directory path.


```yaml
  pcaps:
    - name: pcap:1
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,13"
        socket-mem: "1024"
      port: "ring:1"
      status: "running"
    - name: pcap:2
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,12"
        socket-mem: "1024"
      port: "ring:1"
      out_dir: "/var/log:/var/tmp"
      fsize: 300
      status: "idle"
```

## Update pcap
```image
+++++++++++++++++++++++++++++++++++++++++ Host ++++++++++++++++++++++++++++++
+                                                                           +
+                 -----Pod-----           -------Pod------                  +
------            |  spp-ctl  |           |  spp-primary |                  +
phy:0|            -------------           ----------------                  +
------                                                                      +
phy:1|            -----Pod-----                       ------Pod-------      +
------            |           |                       |              |      +
phy:2|            |           |                       |              |      +
------            |   pcap:1  | ------ ring:1 ------  |   pcap: 2    |      +
+                 |           |                       |              |      +
+                 |           |                       |              |      +
+                 -------------                       ----------------      +
+                                                                           +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```
In order to make this model, create below yaml file named pcap1.yaml

```yaml
apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: pcap1
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
    portmask: "0x07" # needs three ports bound by dpdk
  pcaps:
    - name: pcap:1
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,13"
        socket-mem: "1024"
      port: "ring:1"
      status: "running"
    - name: pcap:2
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,12"
        socket-mem: "1024"
      port: "ring:1"
      out_dir: "/var/log:/var/tmp"
      fsize: 300
      status: "idle"
```
Apply pcap1.yaml
```bash
$ kubectl apply -f pcap1.yaml
```
## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME    CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP     AGE    STATUS
pcap1   1/1   1/1       0/0    0/0   0/0       2/2            k8sn1   10.111.62.237   112s   Pcaps ready ids:1,2
```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp pcap1
Name:         pcap1
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"pcap1","namespace":"default"},"spec":{"ctl":{"image":"sppc/sp...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-03T08:10:27Z
  Generation:          1
  Resource Version:    2927445
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/pcap1
  UID:                 d1ab6202-592c-48da-894e-bf51861b1699
Spec:
  Ctl:
    Image:  sppc/spp-ctl:18.04
    Name:   ctl
  Pcaps:
    Eal:
      Lcores:        1,13
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            pcap:1
    Port:            ring:1
    Status:          running
    Eal:
      Lcores:        1,12
      Socket - Mem:  1024
    Fsize:           300
    Image:           sppc/spp-ubuntu:18.04
    Name:            pcap:2
    out_dir:         /var/log:/var/tmp
    Port:            ring:1
    Status:          idle
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
      Name:   pcap1-ctl-pod
      Phase:  Running
    Status:   1/1
  Events:
    Ctl is created
    Primary is created
    Pcap 1 is created
    Pcap 2 is created
  Mirrors:
    Pods:
    Status:  0/0
  Nfvs:
    Pods:
    Status:  0/0
  Node:      k8sn1
  Pcaps:
    Pods:
      1:
        Name:   pcap1-pcap-1-pod
        Phase:  Running
        Response:
          Client - Id:  1
          Status:       running
      2:
        Name:   pcap1-pcap-2-pod
        Phase:  Running
        Response:
          Client - Id:  2
          Status:       idle
    Status:             2/2
  Primary:
    Pods:
      Name:       pcap1-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.111.62.237
  Status:         Pcaps ready ids:1,2
  Vfs:
    Pods:
    Status:  0/0
Events:      <none>
```

Get all resources of pcap1
```bash
$ kubectl get all -o wide
NAME                    READY   STATUS    RESTARTS   AGE     IP             NODE    NOMINATED NODE   READINESS GATES
pod/pcap1-ctl-pod       1/1     Running   0          2m34s   10.244.1.122   k8sn1   <none>           <none>
pod/pcap1-pcap-1-pod    1/1     Running   0          2m10s   10.244.1.125   k8sn1   <none>           <none>
pod/pcap1-pcap-2-pod    1/1     Running   0          2m10s   10.244.1.124   k8sn1   <none>           <none>
pod/pcap1-primary-pod   1/1     Running   0          2m21s   10.244.1.123   k8sn1   <none>           <none>

NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE     SELECTOR
service/pcap1-ctl-service   ClusterIP   10.111.62.237   <none>        5555/TCP,6666/TCP,7777/TCP   2m33s   pcap1=ctl
```

Show status of the pcap
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.111.62.237
Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > status
- spp-ctl:
  - address: 10.111.62.237:7777
- primary:
  - status: running
- secondary:
  - processes:
    1: pcap:1
    2: pcap:2
spp > pcap 1;status
Basic Information:
  - client-id: 1
  - status: running
  - lcore_ids:
    - master: 1
    - slaves: [13]
Components:
  - core:13 receive
    - rx: ring:1
spp > pcap 2;status
Basic Information:
  - client-id: 2
  - status: idle
  - lcore_ids:
    - master: 1
    - slaves: [12]
Components:
  - core:12 receive
    - rx: ring:1
```


Edit pcap1.yaml file , replace status of pcap:2 like below.

```yaml
      status: "running"
```

Apply pcap1.yaml again.

```bash
$ kubectl apply -f pcap1.yaml
```

Show status of the pcap again.
Pcap:2 status are updated.
```bash
spp > pcap 2;status
Basic Information:
  - client-id: 2
  - status: running
  - lcore_ids:
    - master: 1
    - slaves: [12]
Components:
  - core:12 receive
    - rx: ring:1
```
