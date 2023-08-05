# vfs
Vfs are optional components of spp resource.
Vfs are supported to add new vf and delete old vf.
All components and classifier_table of vf are supported to update too.

## Setup dpdk ports in worker nodes
This example assumes that all worker nodes have set up physical ports using [dpdk][].

[dpdk]:https://doc.dpdk.org/spp/setup/getting_started.html#binding-network-ports-to-dpdk

## Definition of vf
The following defines three vfs.
each vf has a unique name formatted with `vf:<sec-id>`.
the 1st is basic pattern, 2nd vf is vlan pattern
and the last is forward pattern.


```yaml
vfs:
    - name: vf:6
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1-3"
      components:
        - core: 2
          name: "classifier1"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "vhost:0"
          type: "classifier"
        - core: 3
          name: "merger1"
          rx_port:
            - port: "vhost:0"
          tx_port:
            - port: "phy:0"
          type: "merge"
      classifier_table:
         - type: "mac"
           value: "FA:16:3E:7D:CC:36"
           port: "vhost:0"
    - name: vf:9
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,4-5"
      components:
        - core: 4
          name: "classifier44"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "vhost:3"
            - port: "vhost:2"
              vlan:
                operation: "del"
          type: "classifier"
        - core: 5
          name: "merger1"
          rx_port:
            - port: "vhost:3"
            - port: "vhost:2"
              vlan:
                operation: "add"
                #operation: "del"
                id: 66
                pcp: 0
          tx_port:
            - port: "phy:0"
          type: "merge"
      classifier_table:
         - type: "mac"
           value: "FA:16:3E:7D:CC:35"
           port: "vhost:3"
         - type: "vlan"
           vlan: 44
           value: "FA:16:3E:7D:CC:36"
           port: "vhost:2"
    - name: vf:10
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,4-7"
      components:
        - core: 4
          name: "fwd1"
          rx_port:
            - port: "ring:0"
          tx_port:
            - port: "vhost:0"
          type: "forward"
        - core: 5
          name: "fwd2"
          rx_port:
            - port: "vhost:0"
          tx_port:
            - port: "ring:1"
          type: "forward"
        - core: 6
          name: "classifier1"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "ring:0"
          type: "classifier"
        - core: 7
          name: "merger1"
          rx_port:
            - port: "ring:1"
          tx_port:
            - port: "phy:0"
          type: "merge"
      classifier_table:
         - type: "mac"
           value: "FA:16:3E:7D:CC:35"
           port: "ring:0"

```

## Update vf
```image
++++++++++++++++++++++++++++++++++++++++++++++++++ Host +++++++++++++++++++++++++++++++++++
+                                                                                         +
+    -----Pod-----           -------Pod------                                             +
+    |  spp-ctl  |           |  spp-primary |                                             +
+    -------------           ----------------                                             +
-------                                                                                   +
 phy:1|     --------------------------------Pod---------------------------                +
-------     |                                                            |                +
 phy:2|     |                                                            |                +
-------     |                            vf:10                           |                +
+           |                                                            |                +
--------  ------------> [classifier1] ----> ring:0 ------> <fwd1>  --------->             +
 phy:0 |                                                                      vhost:0     +
--------  <------------- (merge1) <-------- ring:1 <------ <fwd2>  <---------             +
+           |                                                            |                +
+           --------------------------------------------------------------                +
+                                                                                         +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
```
In order to make this model, create below yaml file named vf3.yaml

```yaml
apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: vf3
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
  vfs:
    - name: vf:10
      image: sppc/spp-ubuntu:18.04
      eal:
        lcores: "1,4-7"
      components:
        - core: 4
          name: "fwd1"
          rx_port:
            - port: "ring:0"
          tx_port:
            - port: "vhost:0"
          type: "forward"
        - core: 5
          name: "fwd2"
          rx_port:
            - port: "vhost:0"
          tx_port:
            - port: "ring:1"
          type: "forward"
        - core: 6
          name: "classifier1"
          rx_port:
            - port: "phy:0"
          tx_port:
            - port: "ring:0"
          type: "classifier"
        - core: 7
          name: "merger1"
          rx_port:
            - port: "ring:1"
          tx_port:
            - port: "phy:0"
          type: "merge"
      classifier_table:
         - type: "mac"
           value: "FA:16:3E:7D:CC:35"
           port: "ring:0"
```
Apply vf3.yaml
```bash
$ kubectl apply -f vf3.yaml
```
## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME   CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP     AGE   STATUS
vf3    1/1   1/1       0/0    1/1   0/0       0/0            k8sn2   10.97.170.104   34h   Vfs ready ids:10

```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp vf3
Name:         vf3
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"vf3","namespace":"default"},"spec":{"ctl":{"image":"sppc/spp-...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-03T13:38:34Z
  Generation:          7
  Resource Version:    2979279
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/vf3
  UID:                 216544bf-e509-46ef-bff5-ea55e8c03ff4
Spec:
  Ctl:
    Image:  sppc/spp-ctl:18.04
    Name:   ctl
  Primary:
    Eal:
      Lcores:        1
      Socket - Mem:  1024
    Image:           sppc/spp-ubuntu:18.04
    Name:            primary
    Portmask:        0x07
  Vfs:
    classifier_table:
      Port:   ring:0
      Type:   mac
      Value:  FA:16:3E:7D:CC:35
    Components:
      Core:  4
      Name:  fwd1
      rx_port:
        Port:  ring:0
      tx_port:
        Port:  vhost:0
      Type:    forward
      Core:    5
      Name:    fwd2
      rx_port:
        Port:  vhost:0
      tx_port:
        Port:  ring:1
      Type:    forward
      Core:    6
      Name:    classifier1
      rx_port:
        Port:  phy:0
      tx_port:
        Port:  ring:0
      Type:    classifier
      Core:    7
      Name:    merger1
      rx_port:
        Port:  ring:1
      tx_port:
        Port:  phy:0
      Type:    merge
    Eal:
      Lcores:  1,4-7
    Image:     sppc/spp-ubuntu:18.04
    Name:      vf:10
Status:
  Apps:
    Pods:    <nil>
    Status:
  Ctl:
    Pods:
      Name:   vf3-ctl-pod
      Phase:  Running
    Status:   1/1
  Events:
    Ctl is created
    Primary is created
    Vf 10 is created
  Mirrors:
    Pods:
    Status:  0/0
  Nfvs:
    Pods:
    Status:  0/0
  Node:      k8sn2
  Pcaps:
    Pods:
    Status:  0/0
  Primary:
    Pods:
      Name:       vf3-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.97.170.104
  Status:         Vfs ready ids:10
  Vfs:
    Pods:
      10:
        Name:   vf3-vf-10-pod
        Phase:  Running
        Response:
          classifier_table:
            Port:       ring:0
            Type:       mac
            Value:      FA:16:3E:7D:CC:35
            Vlan:       0
          Client - Id:  10
          Components:
            Core:  4
            Name:  fwd1
            rx_port:
              Port:  ring:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            tx_port:
              Port:  vhost:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            Type:           forward
            Core:           5
            Name:           fwd2
            rx_port:
              Port:  vhost:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            tx_port:
              Port:  ring:1
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            Type:           forward
            Core:           6
            Name:           classifier1
            rx_port:
              Port:  phy:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            tx_port:
              Port:  ring:0
              Vlan:
                Id:         0
                Operation:  none
                Pcp:        0
            Type:           classifier
            Core:           7
            Name:           merger1
            rx_port:
              Port:  ring:1
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
            Type:           merge
          Ports:
            phy:0
            phy:1
            phy:2
            vhost:0
            ring:0
            ring:1
    Status:  1/1
Events:      <none>

```

Show status of the vf
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.97.170.104

Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > vf 10 ;status
Basic Information:
  - client-id: 10
  - ports: [phy:0, phy:1, phy:2, vhost:0, ring:0, ring:1]
  - lcore_ids:
    - master: 1
    - slaves: [4, 5, 6, 7]
Classifier Table:
  - FA:16:3E:7D:CC:35, ring:0
Components:
  - core:4 'fwd1' (type: forward)
    - rx: ring:0
    - tx: vhost:0
  - core:5 'fwd2' (type: forward)
    - rx: vhost:0
    - tx: ring:1
  - core:6 'classifier1' (type: classifier)
    - rx: phy:0
    - tx: ring:0
  - core:7 'merger1' (type: merge)
    - rx: ring:1
    - tx: phy:0

```


Edit vf3.yaml file , replace rx_port of core:5 of vf:10 like below.

```yaml
        - core: 5
          name: "fwd2"
          rx_port:
            - port: "vhost:4"
          tx_port:
            - port: "ring:1"
          type: "forward"
```

Apply vf3.yaml again.

```bash
$ kubectl apply -f vf3.yaml

```

Show status of the vf again.
Rx_port are updated.
```bash
spp > vf 10 ;status
Basic Information:
  - client-id: 10
  - ports: [phy:0, phy:1, phy:2, vhost:0, vhost:4, ring:0, ring:1]
  - lcore_ids:
    - master: 1
    - slaves: [4, 5, 6, 7]
Classifier Table:
  - FA:16:3E:7D:CC:35, ring:0
Components:
  - core:4 'fwd1' (type: forward)
    - rx: ring:0
    - tx: vhost:0
  - core:5 'fwd2' (type: forward)
    - rx: vhost:4
    - tx: ring:1
  - core:6 'classifier1' (type: classifier)
    - rx: phy:0
    - tx: ring:0
  - core:7 'merger1' (type: merge)
    - rx: ring:1
    - tx: phy:0

```
