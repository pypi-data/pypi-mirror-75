#!/bin/bash

ip_addr=`hostname -I`

echo $ip_addr

/usr/bin/python3 /spp/src/spp-ctl/spp-ctl -b $ip_addr
