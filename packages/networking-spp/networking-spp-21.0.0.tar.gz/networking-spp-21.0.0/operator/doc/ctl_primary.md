# Ctl and primary
Ctl and primary are basic components of spp resource.

## Create a new basic spp resource
Create a yaml file named primary-vdev.yaml
```bash
$ vi primary-vdev.yaml
```

Write the below to the file and save it.
Spp resource is a kind of custom resources defined by below.
Every component is in spec, also name to identify the resource and image to identify the container image.

```yaml
apiVersion: spp.spp/v1
kind: Spp
metadata:
  name: primary-vdev
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

Here, primary-vdev is the name of the spp resource.
Primary has eal option which represents dpdk options and portmask option.


Apply the file.
```bash
$ kubectl apply -f primary-vdev.yaml
```

## Get list of spp resources
Specify spp to get list of spp resources.
```bash
$ kubectl get spp
NAME           CTL   PRIMARY   NFVS   VFS   MIRRORS   PCAPS   APPS   NODE    SERVICE-VIP     AGE   STATUS
primary-vdev   1/1   1/1       0/0    0/0   0/0       0/0            k8sn3   10.108.95.162   24s   Primary is ready
```

## Get the details of spp resource
Specify spp to get the details of the spp resource.
```bash
$ kubectl describe spp primary-vdev
Name:         primary-vdev
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"spp.spp/v1","kind":"Spp","metadata":{"annotations":{},"name":"primary-vdev","namespace":"default"},"spec":{"ctl":{"image":"...
API Version:  spp.spp/v1
Kind:         Spp
Metadata:
  Creation Timestamp:  2020-02-03T06:57:29Z
  Generation:          1
  Resource Version:    2916785
  Self Link:           /apis/spp.spp/v1/namespaces/default/spps/primary-vdev
  UID:                 c5f7d9e3-fe9b-4aae-bcba-3324e746ecfa
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
      Name:   primary-vdev-ctl-pod
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
  Node:      k8sn3
  Pcaps:
    Pods:
    Status:  0/0
  Primary:
    Pods:
      Name:       primary-vdev-primary-pod
      Phase:      Running
    Status:       1/1
  Service - Vip:  10.108.95.162
  Status:         Primary is ready
  Vfs:
    Pods:
    Status:  0/0
Events:      <none>
```

Also get all resources which the cluster has.
Primary-vdev has two pods and one service below.
```bash
kubectl get all -o wide
NAME                           READY   STATUS    RESTARTS   AGE     IP            NODE    NOMINATED NODE   READINESS GATES
pod/primary-vdev-ctl-pod       1/1     Running   0          4m39s   10.244.3.71   k8sn3   <none>           <none>
pod/primary-vdev-primary-pod   1/1     Running   0          4m27s   10.244.3.72   k8sn3   <none>           <none>

NAME                               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE     SELECTOR
service/primary-vdev-ctl-service   ClusterIP   10.108.95.162   <none>        5555/TCP,6666/TCP,7777/TCP   4m39s   primary-vdev=ctl
```

## Access using spp CLI
Use the IP address of service/primary-vdev-ctl-service to bind primary-vdev.
```bash
$ cd ~/spp/src
$ python3 spp.py -b 10.108.95.162
Welcome to the SPP CLI. Type `help` or `?` to list commands.

spp > status
- spp-ctl:
  - address: 10.108.95.162:7777
- primary:
  - status: running
- secondary:
  - processes:
```

## Update the spp resource
Ctl and primary are not supported to update.

## Delete the spp resource
```bash
$ kubectl delete spp primary-vdev
```
