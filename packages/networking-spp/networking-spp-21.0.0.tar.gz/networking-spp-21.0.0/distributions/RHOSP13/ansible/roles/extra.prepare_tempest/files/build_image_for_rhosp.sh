#!/bin/bash

networking_spp_dir=$PWD
if [ $# -eq 1 ]; then
    networking_spp_dir=$1
fi

networking_spp_ver=1.0.0
home_dir=$networking_spp_dir/networking-spp/devstack/image
dpdk_ver=dpdk-18.02
dpdk_dir=$home_dir/$dpdk_ver
tempest_file=$dpdk_dir/x86_64-native-linuxapp-gcc/app/testpmd
devbind_file=$dpdk_dir/usertools/dpdk-devbind.py

dpdkapp_dir=$home_dir/../../networking_spp/tests/dpdk-app/l2_ping_pong/
dpdkapp_file=$dpdkapp_dir/build/app/l2_ping_pong

function prepare_networking_spp() {
    cd $networking_spp_dir
    git clone -b $networking_spp_ver https://opendev.org/x/networking-spp.git
}

function build_dpdk() {
    sudo yum -y install gcc
    sudo yum -y install glibc-devel
    sudo yum -y install kernel-headers.x86_64 kernel-devel.x86_64
    sudo yum -y install numad.x86_64 numactl-libs.x86_64 numactl-devel.x86_64
    sudo yum -y install libpcap.x86_64 libpcap-devel.x86_64
    sudo yum -y install tuned-profiles-cpu-partitioning.noarch
    sudo yum -y install dpdk-tools.x86_64
    cd $home_dir
    wget http://fast.dpdk.org/rel/$dpdk_ver.tar.gz
    tar xvzf $dpdk_ver.tar.gz
    export RTE_SDK=$home_dir
    export RTE_TARGET=x86_64-native-linuxapp-gcc
    cd $dpdk_dir
    make config T=$RTE_TARGET
    for param in CONFIG_RTE_LIBRTE_KNI CONFIG_RTE_LIBRTE_PMD_KNI CONFIG_RTE_KNI_KMOD CONFIG_RTE_KNI_KMOD_ETHTOOL CONFIG_RTE_KNI_PREEMPT_DEFAULT
    do
        sed -i -e "s/$param=y/$param=n/" build/.config
    done
    sudo make
    ln -s -f build $RTE_TARGET
}

function build_dpdk_app() {
    cd $dpdkapp_dir
    RTE_SDK=$dpdk_dir make

}

function build_image() {
    sudo yum -y install qemu-img kpartx
    sudo curl https://bootstrap.pypa.io/get-pip.py -o $networking_spp_dir/get-pip.py
    sudo python $networking_spp_dir/get-pip.py
    sudo rm $networking_spp_dir/get-pip.py
    sudo pip install django-babel
    sudo pip install virtualenv
    cd $home_dir
    mkdir dib
    cd dib
    virtualenv env
    source env/bin/activate
    git clone -b 2.33.0 https://git.openstack.org/openstack/diskimage-builder
    cd diskimage-builder
    pip install -e .
    cd ../../
    mkdir dib/diskimage-builder/diskimage_builder/elements/install-bin/bin
    cp -a $devbind_file dib/diskimage-builder/diskimage_builder/elements/install-bin/bin
    cp -a $dpdkapp_file dib/diskimage-builder/diskimage_builder/elements/install-bin/bin
    cp -a files/dpdk_setup.sh dib/diskimage-builder/diskimage_builder/elements/install-bin/bin
    cp -a files/init-scripts dib/diskimage-builder/diskimage_builder/elements/dib-init-system/
    disk-image-create ubuntu vm -p python -p make -p coreutils -p gcc -p gcc-multilib -p linux-generic
    sudo mv $home_dir/image.qcow2 $networking_spp_dir
}

function cleanup() {
    cd $networking_spp_dir
    sudo rm -rf networking-spp
    sudo pip uninstall -y virtualenv django-babel pip
}

prepare_networking_spp
build_dpdk
build_dpdk_app
build_image
cleanup
