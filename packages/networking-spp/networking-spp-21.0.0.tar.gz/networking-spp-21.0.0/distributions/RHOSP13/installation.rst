============
Installation
============

This document describes how to install the networking-spp environment. For the networking-spp please refer to the networking-spp-document_.

.. _networking-spp-document: https://networking-spp-yasufum.readthedocs.io/en/latest/index.html

When installing a networking-spp environment, first prepare to install manually, then execute the installation by ansible-playbook.

Manually preparing for installation
===================================

Setting hugepage to grub
------------------------

All procedures in this section are proceeded on Compute nodes.

1. Set the below hugapage related values to variable: ``GRUB_CMDLINE_LINUX`` of file: ``/etc/default/grub`` .

  "default_hugepagesz=1GB hugepagesz=1G hugepages=32 iommu=pt intel_iommu=on user_namespace.enable=1"

example: ``/etc/default/grub``

  GRUB_TIMEOUT=5
  GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
  GRUB_DEFAULT=saved
  GRUB_DISABLE_SUBMENU=true
  GRUB_TERMINAL_OUTPUT="console"
  GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8 crashkernel=auto rhgb quiet default_hugepagesz=1GB hugepagesz=1G hugepages=32 iommu=pt intel_iommu=on user_namespace.enable=1"
  GRUB_DISABLE_RECOVERY="true"

2. Apply hugapage settings to grub according to the overcloud deployment base.

If it is BIOS, apply to file: ``/boot/grub2/grub.cfg`` .

  $ sudo grub2-mkconfig -o /boot/grub2/grub.cfg

If it is UEFI, apply to file: ``/boot/efi/EFI/redhat/grub.cfg`` .

  $ sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg

3. Check if SELinux is enforcing.

  $ getenforce
  Enforcing

4. Reboot compute nodes according to the RHOSP13-reboot-procedure_.

.. _RHOSP13-reboot-procedure: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/director_installation_and_usage/sect-rebooting_the_overcloud#rebooting_compute_nodes

5. Confirm that the 1GB hugepages allocated in ``/proc/meminfo`` .

  $ grep Hugepagesize /proc/meminfo
  Hugepagesize:    1048576 kB


Registering overcloud nodes and attaching the entitlement
---------------------------------------------------------

Perform steps 1 to 4 in chapter 4.5 of director(undercloud)-installation-document_ on each overcloud nodes.

.. _director(undercloud)-installation-document: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/director_installation_and_usage/installing-the-undercloud#registering-and-updating-your-undercloud

Note: This procedure is required for ansible-playbook to execute yum command in each overcloud nodes.

Enabling the rhel-7-server-optional-rpms repository
---------------------------------------------------

Enable the ``rhel-7-server-optional-rpms`` repository on each undercloud and overcloud nodes.

  $ sudo subscription-manager repos --enable rhel-7-server-optional-rpms

Note: The ``rhel-7-server-optional-rpms`` repository is used to install the ``libpcap-devel`` package for DPDK.

Installing SPP and DPDK by specifying the version
-------------------------------------------------

All procedures in this section are proceeded on Compute nodes.
For the details please refer to the SPP-Getting-Started-document_.

.. _SPP-Getting-Started-document: http://doc.dpdk.org/spp-18.05/setup/getting_started.html

1. Remove the originally installed DPDK 18.11.2 version.

  $ sudo yum remove dpdk

2. Disable the ASLR(Address-Space Layout Randomization).

  $ sudo sysctl -w kernel.randomize_va_space=0

3. Clone DPDK repository of version ``18.02`` to any directory (e.g. ``/tmp``).

  $ cd /tmp

  $ git clone -b v18.02 http://dpdk.org/git/dpdk

4. Install required packages to install DPDK.

  $ sudo yum install gcc glibc-devel kernel-headers.x86_64 kernel-devel.x86_64 numad.x86_64 numactl-libs.x86_64 numactl-devel.x86_64 libpcap.x86_64 libpcap-devel.x86_64 tuned-profiles-cpu-partitioning.noarch

5. Open the ``dpdk/config/common_base`` and disable all the kni settings.

example: ``dpdk/config/common_base``

  #

  # Compile librte_kni

  #

  CONFIG_RTE_LIBRTE_KNI=n

  CONFIG_RTE_LIBRTE_PMD_KNI=n

  CONFIG_RTE_KNI_KMOD=n

  CONFIG_RTE_KNI_KMOD_ETHTOOL=n

  CONFIG_RTE_KNI_PREEMPT_DEFAULT=n

6. Check that the symbolic link ``/lib/modules/3.10.0-1062.el7.x86_64/build`` disables because of the uninstallation DPDK ``18.11`` version.

  $ ls -l /lib/modules/3.10.0-1062.el7.x86_64/build
  lrwxrwxrwx. 1 root root 39 Aug  7  2019 /lib/modules/3.10.0-1062.el7.x86_64/build -> /usr/src/kernels/3.10.0-1062.el7.x86_64

Note: If it is disabled, the symbolic link is displayed in red.

7. If the symbolic link is disabled, relink the new symbolic link.

  $ sudo unlink /lib/modules/3.10.0-1062.el7.x86_64/build

  $ ls -l /usr/src/kernels/

  total 4

  drwxr-xr-x. 22 root root 4096 Feb 21 16:28 3.10.0-1062.12.1.el7.x86_64

  $ sudo ln -s /usr/src/kernels/3.10.0-1062.12.1.el7.x86_64/ /lib/modules/3.10.0-1062.el7.x86_64/build

  $ ls -l /lib/modules/3.10.0-1062.el7.x86_64/build

  lrwxrwxrwx. 1 root root 45 Feb 21 16:45 /lib/modules/3.10.0-1062.el7.x86_64/build -> /usr/src/kernels/3.10.0-1062.12.1.el7.x86_64/

8. Change directory to DPDK. And export environment variables ``RTE_SDK`` and ``RTE_TARGET``.

  $ cd dpdk

  $ export RTE_SDK=$(pwd)

  $ export RTE_TARGET=x86_64-native-linuxapp-gcc

9. Execute ``make install`` with environment variable ``RTE_TARGET``.

  $ make install T=$RTE_TARGET

10. If the result of the above step 9 is the kni error, Open the ``x86_64-native-linuxapp-gcc/.config`` and disable all the kni settings.

example: ``x86_64-native-linuxapp-gcc/.config``

  #

  # Compile librte_kni

  #

  CONFIG_RTE_LIBRTE_KNI=n

  CONFIG_RTE_LIBRTE_PMD_KNI=n

  CONFIG_RTE_KNI_KMOD=n

  CONFIG_RTE_KNI_KMOD_ETHTOOL=n

  CONFIG_RTE_KNI_PREEMPT_DEFAULT=n

11. Execute ``make install`` again.

  $ make install T=$RTE_TARGET

Note: Don't execute ``make clean``. Otherwise, ``x86_64-native-linuxapp-gcc/.config`` is removed.

12. Clone SPP repository of version ``18.02`` to any directory (e.g. ``/tmp``).

  $ cd /tmp

  $ git clone -b v18.02 http://dpdk.org/git/apps/spp

13. Change directory to SPP.

  $ cd spp

14. Append the Setting ``CFLAGS += -std=gnu99`` to the following files.

・``src/nfv/Makefile``

・``src/primary/Makefile``

・``src/vm/Makefile``

15. Append the Setting ``CFLAGS += -Wno-error=missing-prototypes`` to ``src/vf/Makefile``.

16. Execute ``make``

  $ make

17. Perform chapter 1.3 to 1.4 of SPP-Getting-Started-document_ . And chack the following points.

・It is to be able to bind a port for DPDK.

・It is to be able to monitor packets by the ``l2fwd``.

example: ``packets monitor of l2fwd``

  Port statistics ====================================

  Statistics for port 0 ------------------------------

  Packets sent:                        0

  Packets received:                    0

  Packets dropped:                     0

  Aggregate statistics ===============================

  Total packets sent:                  0

  Total packets received:              0

  Total packets dropped:               0

  ====================================================

Note: When you execute ``insmod`` with ``igb_uio.ko`` on step 1.3.1, replase the file path ``kmod/igb_uio.ko`` to actual path.

  $ find /tmp/dpdk -name igb_uio.ko

  /tmp/dpdk/x86_64-native-linuxapp-gcc/build/lib/librte_eal/linuxapp/igb_uio/igb_uio.ko

  /tmp/dpdk/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko

  $ sudo insmod /tmp/dpdk/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko


18. Rebind the port that bound on the above step 17, to the kernel driver ``i40e``.

  $ sudo $RTE_SDK/usertools/dpdk-devbind.py --bind=i40e ``PCI address``

Setting the environment variable "LANG"
---------------------------------------


Installation by ansible-playbook
================================

In this section, install networking-spp environment by ansible-playbook.

1. Set the environment variable ``LANG`` in the host that execute ansible-playbook, to ``en_US.UTF-8``.

  $ export LANG=en_US.UTF-8

Note: Remember the original value of ``LANG`` before the setting.

  $ echo $LANG

  ja_JP.UTF-8

2. Set each IP addresses or host names to variables: ``undercloud`` , ``controller`` and ``compute`` of file: ``hosts`` in this installer.

example: ``hosts``

  ################ Edit below IP addresses or host names as needed #################
  # controller nodes
  [controller]
  192.168.24.8

  # compute nodes
  [compute]
  192.168.24.10

  # an undercloud(director) node
  [undercloud]
  127.0.0.1

  ########################### Don't edit below variables ###########################
  # group overcloud nodes
  [overcloud:children]
  controller
  compute

Note: Don't edit in the section: ``Don't edit below variables`` .

3. Set values for each variables in all files in the directory: ``group_vars`` in this installer according to your environment.

example: ``group_vars/overcloud.yml``

  ---
  ############################################################
  # name: overcloud.yml
  # description: Setting variables used in overcloud group.
  ############################################################

  ######################### Edit below variables as needed #########################
  # client port of ETCD service
  etcd_client_port: 2379

  # peer port of ETCD service
  etcd_peer_port: 2380

  # ssh login account
  ansible_ssh_user: heat-admin

  ########################### Don't edit below variables ###########################
  # networking-spp installation path at container
  networking_spp_dir: /opt

  # service name of SPP agent
  spp_agent_service_name: q-spp-agt

  # neutron config file path at host
  neutron_conf_path: /var/lib/config-data/puppet-generated/neutron/etc/neutron/neutron.conf

  # ML2 config file path at host
  ml2_conf_path: /var/lib/config-data/puppet-generated/neutron/etc/neutron/plugins/ml2/ml2_conf.ini

Note: Don't edit in the section: ``Don't edit below variables`` in each files.


4. Execute installation by ansible-playbook.

  $ ansible-playbook -i hosts install_networking-spp.yml

Note: uninstallation by ansible-playbook uses variables set in file: ``hosts`` and all files in the directory: ``group_vars`` in this installer. So don't edit all variables after installation.

5. Set the environment variable ``LANG`` that set on the above step 1, to the original value.

  $ export LANG=``original value``


Replacing the "nova_libvirt" container
======================================

On the networking-spp environment on RHEL compute nodes, you must bind the directory ``/tmp`` on the host to the ``nova_libvirt`` container.
The directory is used to create sockets for vhostusers by SPP.

All procedures in this section are proceeded on Compute nodes.

1. Stop the ``nova_libvirt`` container.

  $ sudo docker stop nova_libvirt

2. Change the ``nova_libvirt`` container name (e.g. ``nova_libvirt_bk``).

  $ sudo docker rename nova_libvirt nova_libvirt_bk

3. Get the command that create the ``nova_libvirt`` container.

  $ sudo paunch debug --file /var/lib/tripleo-config/hashed-docker-container-startup-config-step_3.json --container nova_libvirt --action print-cmd

4. Append the ``--volume=/tmp:/tmp`` option to the command that got on above step 3, and create the new ``nova_libvirt`` container with the command.

  $ sudo docker run --name nova_libvirt --detach=true --env=KOLLA_CONFIG_STRATEGY=COPY_ALWAYS --env=TRIPLEO_CONFIG_HASH=74ca18c078dd0d6e3371af0610b02bcd --net=host --pid=host --privileged=true --restart=always --volume=/etc/hosts:/etc/hosts:ro --volume=/etc/localtime:/etc/localtime:ro --volume=/etc/pki/ca-trust/extracted:/etc/pki/ca-trust/extracted:ro --volume=/etc/pki/ca-trust/source/anchors:/etc/pki/ca-trust/source/anchors:ro --volume=/etc/pki/tls/certs/ca-bundle.crt:/etc/pki/tls/certs/ca-bundle.crt:ro --volume=/etc/pki/tls/certs/ca-bundle.trust.crt:/etc/pki/tls/certs/ca-bundle.trust.crt:ro --volume=/etc/pki/tls/cert.pem:/etc/pki/tls/cert.pem:ro --volume=/dev/log:/dev/log --volume=/etc/ssh/ssh_known_hosts:/etc/ssh/ssh_known_hosts:ro --volume=/etc/puppet:/etc/puppet:ro --volume=/var/lib/kolla/config_files/nova_libvirt.json:/var/lib/kolla/config_files/config.json:ro --volume=/var/lib/config-data/puppet-generated/nova_libvirt/:/var/lib/kolla/config_files/src:ro --volume=/etc/ceph:/var/lib/kolla/config_files/src-ceph:ro --volume=/lib/modules:/lib/modules:ro --volume=/dev:/dev --volume=/run:/run --volume=/sys/fs/cgroup:/sys/fs/cgroup --volume=/var/lib/nova:/var/lib/nova:shared --volume=/etc/libvirt:/etc/libvirt --volume=/var/run/libvirt:/var/run/libvirt --volume=/var/lib/libvirt:/var/lib/libvirt --volume=/var/log/containers/libvirt:/var/log/libvirt --volume=/var/log/libvirt/qemu:/var/log/libvirt/qemu:ro --volume=/var/lib/vhost_sockets:/var/lib/vhost_sockets --volume=/sys/fs/selinux:/sys/fs/selinux --volume=/tmp:/tmp 192.168.24.1:8787/rhosp13/openstack-nova-libvirt:13.0-105.1568971378

