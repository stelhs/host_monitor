#!/bin/bash

date=`date "+%Y%m%d_%H%M%S"`
dest_folder=/backup/mirror
log_folder=/backup/

exclude="--exclude alpein_software "
#exclude+="--exclude cloudsecurium_ovas "

/root/host_monitor/tgadm.py "Run Raid1 backup"

echo "start rsync: "`date "+%Y-%m-%d %H:%M:%S"` >> $log_folder/mirror_backup_duration
rsync -avAX /storage/ $dest_folder/ --log-file $log_folder/mirror_backup_log $exclude --delete
rsync_ret_code=$?
echo "finished rsync: "`date "+%Y-%m-%d %H:%M:%S"` >> $log_folder/mirror_backup_duration

if [ $rsync_ret_code -eq '0' ]
then
	/root/host_monitor/tgadm.py "raid1 mirror backup $date finished successfully"
else
	/root/host_monitor/tgadm.py "raid1 mirror backup $date failed"
fi
