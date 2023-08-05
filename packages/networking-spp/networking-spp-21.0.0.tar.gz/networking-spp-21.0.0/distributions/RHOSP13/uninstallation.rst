==============
Uninstallation
==============

This document describes how to uninstall the networking-spp environment.
When uninstalling a networking-spp environment, first execute the uninstallation by ansible-playbook, then perform to remaining procedures manually.

Uninstallation by ansible-playbook
==================================

Execute uninstallation by ansible-playbook.

  $ ansible-playbook -i hosts uninstall_networking-spp.yml

Manually performing for uninstallation
======================================

Restoring the nova_libvirt container
--------------------------------

All procedures in this section are proceeded on Compute nodes.

1. Stop the existing ``nova_libvirt`` container.

  $ sudo docker stop nova_libvirt

2. Remove the existing ``nova_libvirt`` container.

  $ sudo docker rm nova_libvirt

3. Rename the original ``nova_libvirt_bk`` container to ``nova_libvirt``.

  $ sudo docker rename nova_libvirt_bk nova_libvirt

4. Start the original ``nova_libvirt`` container.

  $ sudo docker start nova_libvirt


Uninstalling SPP and DPDK
-------------------------

All procedures in this section are proceeded on Compute nodes.

1. Check environment variables ``RTE_SDK`` and ``RTE_TARGET``.

  $ echo $RTE_SDK

  /tmp/dpdk


  $ echo $RTE_TARGET

  x86_64-native-linuxapp-gcc

Note: If their variables have been deleted, set values to them again.

2. Change directory to SPP.

  $ cd /tmp/spp

3. Execute ``make clean``

  $ make clean

4. Change directory to DPDK.

  $ cd /tmp/spp

5. Create the symbolic link.

  $ ln -s -f $RTE_TARGET build

Note: This setting is required to use the ``build`` directory on the ``make clean`` command.

6. Execute ``make clean``

  $ make clean

7. Remove all SPP and DPDK files

  $ rm -r /tmp/spp

  $ rm -r /tmp/dpdk

8. Role back DPDK to the originally installed 18.11.2 verion.

  $ sudo yum install dpdk-18.11.2-1.el7.x86_64

Unsetting hugepage from grub
----------------------------

All procedures in this section are proceeded on Compute nodes.

1. Unset the below hugapage related values from variable: ``GRUB_CMDLINE_LINUX`` of file: ``/etc/default/grub`` .

  "default_hugepagesz=1GB hugepagesz=1G hugepages=32 iommu=pt intel_iommu=on user_namespace.enable=1"

example: ``/etc/default/grub``

  GRUB_TIMEOUT=5
  GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
  GRUB_DEFAULT=saved
  GRUB_DISABLE_SUBMENU=true
  GRUB_TERMINAL_OUTPUT="console"
  GRUB_CMDLINE_LINUX="console=tty0 console=ttyS0,115200n8 crashkernel=auto rhgb quiet"
  GRUB_DISABLE_RECOVERY="true"

2. Apply hugapage unsettings to grub according to the overcloud deployment base.

If it is BIOS, apply to file: ``/boot/grub2/grub.cfg`` .

  $ sudo grub2-mkconfig -o /boot/grub2/grub.cfg

If it is UEFI, apply to file: ``/boot/efi/EFI/redhat/grub.cfg`` .

  $ sudo grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg

3. Reboot compute nodes according to the RHOSP13-reboot-procedure_.

.. _RHOSP13-reboot-procedure: https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html/director_installation_and_usage/sect-rebooting_the_overcloud#rebooting_compute_nodes

4. Confirm that the 2MB hugepages allocated in ``/proc/meminfo`` .

  $ grep Hugepagesize /proc/meminfo
  Hugepagesize:       2048 kB

