# spp-operator
spp-operator
## Overview

The spp operator manages spp resource deployed to Kubernetes and automates tasks related to operating [spp][]

[spp]:https://doc.dpdk.org/spp/

Spp resource is a kind of Custom Resource Definition(CRD) composed of components below.

- [Ctl and primary](./doc/ctl_primary.md)
- [Nfvs](./doc/nfvs.md)
- [Vfs](./doc/vfs.md)
- [Mirrors](./doc/mirrors.md)
- [Pcaps](./doc/pcaps.md)


## Requirements
- DPDK 18.08
- SPP stable-v18.08
- Kubernetes 1.17+
- Docker 18.9+
- Golang 1.13.3
- Operator-SDK 0.13.0

## Install
See the [Install](./doc/install_guide.md)

## Usage
See the [Usage](./doc/usage.md)

## Test
See the [Test](./doc/test.md)
