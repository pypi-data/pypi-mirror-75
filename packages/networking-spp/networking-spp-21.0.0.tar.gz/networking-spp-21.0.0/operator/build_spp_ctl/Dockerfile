FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install eventlet bottle netaddr
RUN git clone http://dpdk.org/git/apps/spp -b v18.08.4
ADD start-spp-ctl.sh /root/start-spp-ctl.sh
RUN chmod 755 /root/start-spp-ctl.sh
