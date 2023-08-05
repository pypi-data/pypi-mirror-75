# mirrors
Mirrors are optional components of spp resource.
Mirrors are supported to add new mirror and delete old mirror.
All components of mirror are supported to update too.

## Setup dpdk ports in worker nodes
This example assumes that all worker nodes have set up physical ports using [dpdk][].

[dpdk]:https://doc.dpdk.org/spp/setup/getting_started.html#binding-network-ports-to-dpdk

## Definition of mirror
The following defines two mirrors.
each mirror has a unique name formatted with `mirror:<sec-id>`.
the 1st is basic pattern, 2nd mirror has 2 tx ports.


```yaml
  mirrors:
    - name: mirror:13
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,8-9"
      components:
        - core: 8
          name: "mirror1"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "vhost:1"
          type: "mirror"
        - core: 9
          name: "mirror2"
          rx_port:
            - port: "vhost:1"
          tx_port:
            - port: "phy:0"
          type: "mirror"
    - name: mirror:14
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,10-11"
      components:
        - core: 10
          name: "mirror3"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "vhost:1"
            - port: "vhost:2"
          type: "mirror"
        - core: 11
          name: "mirror4"
          rx_port:
            - port: "vhost:1"
          tx_port:
            - port: "phy:0"
            - port: "phy:1"
          type: "mirror"

```

## Update mirror
```image
++++++++++++++++++++++++ Host ++++++++++++++++++++++++++++++++++
+                                                              +
+    -----Pod-----           -------Pod------                  +
+    |  spp-ctl  |           |  spp-primary |                  +
+    -------------           ----------------                  +
-------                                                        +
 phy:1|     -----------------Pod-------------                  +
-------     |                               |                  +
 phy:2|     |       mirror :13              |                  +
-------     |                               |                  +
+           |                               |                  +
--------  ------------>  [mirror1]  --------->                 +
 phy:0 |                                        vhost:1        +
--------  <------------- [mirror2]  <---------                 +
+           |                               |                  +
+           ---------------------------------                  +
+                                                              +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```
In order to make this model, create below yaml file named mirror1.yaml

```yaml

apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: mirror1
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
  mirrors:
    - name: mirror:13
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,8-9"
      components:
        - core: 8
          name: "mirror1"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "vhost:1"
          type: "mirror"
        - core: 9
          name: "mirror2"
          rx_port:
            - port: "vhost:1"
          tx_port:
            - port: "phy:0"
          type: "mirror"
```
Apply mirror1.yaml
```bash
$ kubectl apply -f mirror1.yaml
```
## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME      CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP    AGE   STATUS
mirror1   1/1   1/1       0/0    0/0   1/1       0/0            k8sn1   10.96.56.202   47s   Mirrors ready ids:13
```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp mirror1
Name:         mirror1
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"mirror1","namespace":"default"},"spec":{"ctl":{"image":"sppc/...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-05T00:34:01Z
  Generation:          1
  Resource Version:    3270368
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/mirror1
  UID:                 774a92a1-ff54-4afa-9b94-f51c1f620602
Spec:
  Ctl:
    Image:  sppc/spp-ctl:18.04
    Name:   ctl
  Mirrors:
    Components:
      Core:  8
      Name:  mirror1
      rx_port:
        Port:  phy:0
      tx_port:
        Port:  vhost:1
      Type:    mirror
      Core:    9
      Name:    mirror2
      rx_port:
        Port:  vhost:1
      tx_port:
        Port:  phy:0
      Type:    mirror
    Eal:
      Lcores:  1,8-9
    Image:     sppc/spp-ubuntu:18.04
    Name:      mirror:13
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
      Name:   mirror1-ctl-pod
      Phase:  Running
    Status:   1/1
  Events:
    Ctl is created
    Primary is created
    Mirror 13 is created
  Mirrors:
    Pods:
      13:
        Name:   mirror1-mirror-13-pod
        Phase:  Running
        Response:
          classifier_table:  <nil>
          Client - Id:       13
          Components:
            Core:  8
            Name:  mirror1
            rx_port:
              Port:  phy:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            tx_port:
              Port:  vhost:1
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            Type:           mirror
            Core:           9
            Name:           mirror2
            rx_port:
              Port:  vhost:1
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            tx_port:
              Port:  phy:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            Type:           mirror
          Ports:
            phy:0
            phy:1
            phy:2
            vhost:1
    Status:  1/1
  Nfvs:
    Pods:
    Status:  0/0
  Node:      k8sn1
  Pcaps:
    Pods:
    Status:  0/0
  Primary:
    Pods:
      Name:       mirror1-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.96.56.202
  Status:         Mirrors ready ids:13
  Vfs:
    Pods:
    Status:  0/0
Events:      <none>
```

Show status of the mirror
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.96.56.202
Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > mirror 13; status
Basic Information:
  - client-id: 13
  - ports: [phy:0, phy:1, phy:2, vhost:1]
  - lcore_ids:
    - master: 1
    - slaves: [8, 9]
Components:
  - core:8 'mirror1' (type: mirror)
    - rx: phy:0
    - tx: [vhost:1]
  - core:9 'mirror2' (type: mirror)
    - rx: vhost:1
    - tx: [phy:0]
```

Edit mirror1.yaml file , replace rx_port of core:9 of mirror:13 like below.

```yaml
  - core:9 'mirror2' (type: mirror)
    - rx: vhost:2
    - tx: [phy:0]
```

Apply mirror1.yaml again.

```bash
$ kubectl apply -f mirror1.yaml

```

Show status of the mirror again.
Rx_port are updated.
```bash
Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > mirror 13;status
Basic Information:
  - client-id: 13
  - ports: [phy:0, phy:1, phy:2, vhost:1, vhost:2]
  - lcore_ids:
    - master: 1
    - slaves: [8, 9]
Components:
  - core:8 'mirror1' (type: mirror)
    - rx: phy:0
    - tx: [vhost:1]
  - core:9 'mirror2' (type: mirror)
    - rx: vhost:2
    - tx: [phy:0]
```

