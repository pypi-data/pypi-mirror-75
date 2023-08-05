============
Requirements
============

This document describes requirements to install networking-spp environment by this installer.

OS version
==========
Supported OS is ``RHEL 7.7`` .

.. application_list:

Application list
================

A list of applications used by this installer is shown with a brief description.
Unless otherwise specified, they are RPM packages.

+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| name                              | version | description                                                                                                                                                              |
+===================================+=========+==========================================================================================================================================================================+
| Ansible                           | 2.6.11  | It is provided to undercloud node by RedHat.                                                                                                                             |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| diskimage-builder(manually using) | 2.33.0  | It is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                         |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| django-babel                      | 0.6.2   | It is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                         |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Docker                            | 1.13.1  | It is provided to each overcloud nodes by undercloud node.                                                                                                               |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DPDK(manually building)           | 18.02   | It is provided by the DPDK git.                                                                                                                                          |
|                                   |         | This version is manually installed to compute nodes by you, and replaces 18.11.2 version provided by undercloud node.                                                    |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| dpdk-tools                        | 18.11.2 | It is provided by the RedHat. It is temporarily installed to undercloud node by this installer to create an image for tempest.                                           |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| etcd                              | 3.2.26  | It is provided to controller node by undercloud node.                                                                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| etcd3(pip package)                | 0.11.1  | It is installed to overcloud nodes by this installer.                                                                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| etcd3gw(pip package)              | 0.2.5   | It is installed to overcloud nodes by this installer.                                                                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| gcc                               | 4.8.5   | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| glibc-devel                       | 2.17    | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| iptables                          | 1.4.21  | It is provided to a controller node by undercloud node.                                                                                                                  |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| kernel-devel                      | 3.10.0  | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| kernel-headers                    | 3.10.0  | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| libcap-devel                      | 2.22    | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| libpcap                           | 1.5.3   | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| libpcap-devel                     | 1.5.3   | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| numactl-devel                     | 2.0.12  | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| numactl-libs                      | 2.0.12  | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| numad                             | 0.5     | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tuned-profiles-cpu-partitioning   | 2.11.0  | It is provided by the RedHat. It is manually installed to compute nodes by you to make SPP ans DPDK environments.                                                        |
|                                   |         | Also it is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| networking-spp(manually building) | 1.0.0   | It is installed to overcloud nodes by this installer.                                                                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| pip(pip package)                  | 20.0.2  | It is installed to overcloud nodes by this installer.                                                                                                                    |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| python                            | 2.7.5   | It is provided to undercloud node by RedHat.                                                                                                                             |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| selinux-policy-devel              | 3.13.1  | It is temporarily installed to undercloud node by this installer to register new selinux policies.                                                                       |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| SPP(manually building)            | 18.02   | It is provided by the SPP git. It is manually installed to compute nodes by you.                                                                                         |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| virtualenv                        | 15.1.0  | It is temporarily installed to undercloud node by this installer to create an image for tempest.                                                                         |
+-----------------------------------+---------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Container list
==============

A list of containers used by this installer is shown with a brief description.

+-------------------+-------------------------------------+---------------------+------------+----------------------------------------------------------------------------+
| name              | source image                        | version             | node       | description                                                                |
+===================+=====================================+=====================+============+============================================================================+
| neutron_api       | openstack-neutron-server            | 13.0-93             | controller | It is rebooted by this installer to apply a ML2 config file,               |
|                   |                                     |                     |            | and installed netwotking-spp files to use a spp mechanism driver.          |
+-------------------+-------------------------------------+---------------------+------------+----------------------------------------------------------------------------+
| neutron_ovs_agent | openstack-neutron-openvswitch-agent | 13.0-92             | compute    | It is rebooted by this installer to apply a ML2 config file.               |
+-------------------+-------------------------------------+---------------------+------------+----------------------------------------------------------------------------+
| nova_compute      | openstack-nova-compute              | 13.0-102.1568973092 | compute    | It is rebooted by this installer to apply a nova config file.              |
+-------------------+-------------------------------------+---------------------+------------+----------------------------------------------------------------------------+
| nova_libvirt      | openstack-nova-libvirt              | 13.0-105.1568971378 | compute    | It is manually rebooted by you to bind a directory used by the SPP driver. |
+-------------------+-------------------------------------+---------------------+------------+----------------------------------------------------------------------------+

Execution environment
=====================

Fulfill the following requirements before using this installer.

* It is the environment that be able to connect to the internet by no proxy.

* It is that the platform of each undercloud and overcloud nodes are ``RHOSP 13`` .

* It is that the following applications provided by RedHat are installed. (Refer :ref:`application_list` for their versions and target nodes.)
  * Ansible
  * Docker
  * etcd
  * iptables
  * python

* It is no problem that DPDK 18.02 version replaces 18.11.2 version installed on each compute nodes.
  * Note: Don't install services that use DPDK 18.11.2 version (e.g. OVS-DPDK).

* It is that the number of controller nodes is only one. (On the one hand, compute nodes can be multiple counts.)

