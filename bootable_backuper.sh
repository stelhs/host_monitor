#!/bin/bash

trap '/root/host_monitor/tgadm.py "bootable backup interrupted"' INT

if [ ! -d "/media/root-ro" ]
then
    /root/host_monitor/tgadm.py "Bootable backup was not started because rootfs is RW. Switch root to RO and try again."
    echo "Bootable backup was not started because rootfs is RW. Switch root to RO and try again."
    exit 1
fi

/root/host_monitor/tgadm.py "starting bootable backup"

dd if=/dev/sdd conv=sync,noerror bs=64K status=progress | gzip -c > /backup/bootable_sr90.img.gz_incomplete
if [ $? -eq '0' ]
then
    mv /backup/bootable_sr90.img.gz_incomplete /backup/bootable_sr90.img.gz
    /root/host_monitor/tgadm.py "finished bootable_sr90.img.gz"
else
    /root/host_monitor/tgadm.py "bootable backup failed"
fi

# for restore:
# gunzip -c /backup/bootable_sr90.img.gz | dd of=/dev/YOUR-DEVICE-DONT-EFF-THIS-UP conv=sync,noerror bs=64K status=progress
