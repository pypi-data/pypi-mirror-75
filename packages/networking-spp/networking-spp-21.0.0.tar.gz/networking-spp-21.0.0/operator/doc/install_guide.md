# Installation guide

## Set up a kubernetes cluster which has a single master node and a single worker node.
Spp operator only supports a single worker node currently.

### The specification of a master node
- OS Ubuntu 18.04
- CPU Core 2+
- Memory 4G+
- Disk 30G+
- NIC 1+

### The specification of a worker node
- OS Ubuntu 18.04
- CPU Core 16+
- Memory 20G+
- Disk 200G+
- NIC 1+

### Supported software version
- DPDK v18.08 + SPP v18.08.4 or  
  DPDK v20.02 + SPP v20.02
- Kubernetes 1.17
- Docker 18.09
- golang 1.13.3
- operator-sdk 0.13.0

### Set up common

#### Disable swap
```bash
$ sudo swapoff -a
```

#### Install docker
```bash
$ sudo apt update && apt upgrade
$ sudo apt install -y docker.io=18.09.7-0ubuntu1~18.04.4
$ sudo gpasswd -a $USER docker
```

#### Set up the docker network if needs
The default CIDR of docker network is 172.17.0.1/16.
Following the steps below if you want to change it.
```bash
$ sudo vi /lib/systemd/system/docker.service
```

Add --bip option like below
```bash
ExecStart=/usr/bin/dockerd => ExecStart=/usr/bin/dockerd \ --bip=10.0.0.1/16
```

Restart docker daemon
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart docker
```

#### Install kubeadm and kubelet
```bash
$ apt-get update && apt-get install -y apt-transport-https curl
$ curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
$ cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
  deb https://apt.kubernetes.io/ kubernetes-xenial main
  EOF
$ apt-get update
$ apt-get install -y kubelet=1.17.6-00 kubeadm=1.17.6-00 kubectl=1.17.6-00
$ apt-mark hold kubelet kubeadm kubectl
```
Reference: <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/>

### Set up a master node
Set up kubeadm using specified flannel pod CIDR
```bash
$ kubeadm init --pod-network-cidr=10.244.0.0/16
```
Set up config to access kube-apiserver
```bash
$ mkdir -p $HOME/.kube
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
Set up flannel CNI
```bash
$ kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/2140ac876ef134e0ed5af15c65e414cf26827915/Documentation/kube-flannel.yml
```
Reference: <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>

### Set up a worker node
Make the worker node join the cluster
```bash
$ kubeadm join <control-plane-host>:<control-plane-port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```
Reference: <https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/>

## Set up Huge page and make the container images in the worker node
Do the following steps in the worker node.
### Set up Huge Page
Reference: <https://doc.dpdk.org/spp/setup/getting_started.html>
Note that only 1G hugepage is supported.
### Make the container images
#### Clone the repositories of dpdk, spp and spp operator
```bash
$ cd ~
$ git clone -b v18.08 http://dpdk.org/git/dpdk  # or '-b v20.02'
$ git clone -b v18.08.4 http://dpdk.org/git/apps/spp  # or '-b v20.02'
$ git clone http://opendev.org/x/networking-spp
```
#### Apply a patch to Dockerfile

- Note: This is not necessary if you use SPP v20.02.

```bash
$ cd ~/spp
```
Save the following as a file named diff.patch.
```text
diff --git a/tools/sppc/build/ubuntu/spp/Dockerfile.18.04 b/tools/sppc/build/ubuntu/spp/Dockerfile.18.04
index 2257747..e7f21dc 100644
--- a/tools/sppc/build/ubuntu/spp/Dockerfile.18.04
+++ b/tools/sppc/build/ubuntu/spp/Dockerfile.18.04
@@ -20,6 +20,8 @@ ENV PATH ${home_dir}/${spp_dir}/src/primary/${rte_target}/:${PATH}
 ENV PATH ${home_dir}/${spp_dir}/src/nfv/${rte_target}/:${PATH}
 ENV PATH ${home_dir}/${spp_dir}/src/vf/${rte_target}/:${PATH}
 ENV PATH ${home_dir}/${spp_dir}/src/vm/${rte_target}/:${PATH}
+ENV PATH ${home_dir}/${spp_dir}/src/mirror/${rte_target}/:${PATH}
+ENV PATH ${home_dir}/${spp_dir}/src/pcap/${rte_target}/:${PATH}
 ENV DEBIAN_FRONTEND noninteractive

 RUN apt-get update && apt-get install -y \
```
Apply it
```bash
$ git apply diff.patch
```

#### Make the image of spp container
```bash
$ cd ~/spp/tools/sppc
$ python build/main.py -t spp --dist-ver 18.04 --dpdk-branch v18.08 --spp-branch v18.08.4
## or if you use v20.02
#$ python build/main.py -t spp --dist-ver 18.04 --dpdk-branch v20.02 --spp-branch v20.02
```

#### Make the image of dpdk container
```bash
$ cd ~/spp/tools/sppc
$ python build/main.py -t dpdk --dist-ver 18.04 --dpdk-branch v18.08
## or if you use v20.02
#$ python build/main.py -t dpdk --dist-ver 18.04 --dpdk-branch v20.02
```

#### Make the image of spp-ctl container
```bash
$ cd ~/networking-spp/operator/build_spp_ctl
$ docker build . -t sppc/spp-ctl:18.04
```
- Note: If you use SPP v20.02, modify ~/networking-spp/oprator/build_spp_ctl/Dockerfile before executing docker build.

```
-RUN git clone http://dpdk.org/git/apps/spp -b v18.08.4
+RUN git clone http://dpdk.org/git/apps/spp -b v20.02
```

## Set up golang and Operator SDK in the master node
Do the following steps in the master node.
### Install golang
```bash
$ wget https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz
$ sudo tar -C /usr/local/ -xzf go1.13.3.linux-amd64.tar.gz
$ sudo rm /usr/bin/go; sudo ln -s /usr/local/go/bin/go /usr/bin/go
```
### Set up golang home
```bash
$ cat <<EOF >>.bashrc
$ export GOPATH=$HOME/go
  EOF
$ source ~/.bashrc
```

### Install Operator SDK
```bash
$ RELEASE_VERSION=v0.13.0
$ curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${RELEASE_VERSION}/operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu
$ chmod +x operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu && sudo mkdir -p /usr/local/bin/ && sudo cp operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu /usr/local/bin/operator-sdk && rm operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu
```
Reference: <https://github.com/operator-framework/operator-sdk/blob/v0.13.0/doc/user-guide.md>

## Set up spp operator and make Custom Resource Definition(CRD) in the master nodes
### Set up spp operator
```bash
$ mkdir -p $GOPATH/src/opendev.org/x
$ cd $GOPATH/src/opendev.org/x
$ git clone https://opendev.org/x/networking-spp
```

### Make the CRD of spp
```bash
$ cd $GOPATH/src/opendev.org/x/networking-spp/operator
$ kubectl apply -f deploy/crds/spp.spp_crd.yaml
```
