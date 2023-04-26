import re
from MonitorBase import *

class MdMonitor(MonitorBase):
    def __init__(s, hm):
        super().__init__(hm, "MdMonitor")


    def mdstat(s):
        with open('/proc/mdstat', 'r') as f:
            rows = f.read().split('\n')

        if len(rows) < 3:
            return {'state': 'no_exist'}

        if len(rows) >= 3:
            matches = re.findall('resync[ ]+=[ ]+([0-9\.]+)\%', rows[3])
            if len(matches):
                return {'state': 'resync',
                        'progress': matches[0]}

            matches = re.findall('/recovery[ ]+=[ ]+([0-9\.]+)\%/', rows[3])
            if len(matches):
                return {'state': 'recovery',
                        'progress': matches[0]}

        matches = re.findall("\[[U_]+\]", rows[2])
        if not len(matches):
            return {'state': 'no_exist'}
        mode = matches[0]

        if mode == '[UU]':
            return {'state': 'normal'};

        if mode == '[_U]' or mode == '[U_]':
            return {'state': 'damage'};

        return {'state': 'parse_err'};


    def do(s):
        abnormal = False
        while(1):
            stat = s.mdstat()
            if stat['state'] == 'normal':
                if abnormal:
                    s.log.info("RAID1 recovered")
                    s.toAdmin("RAID1 recovered")
                abnormal = False
                Task.sleep(60000, "normal")
                continue

            if stat['state'] == 'parse_err':
                s.log.err("mdadm parse error")
                s.toAdmin('mdadm parse error')
                abnormal = True
                Task.sleep(60000, "parse_err")
                continue

            if stat['state'] == 'damage':
                s.log.err("RAID1 damage")
                s.toAdmin('RAID1 damage')
                abnormal = True
                Task.sleep(900000, "damage")
                continue

            if stat['state'] == 'no_exist':
                s.log.err("RAID1 no exist")
                s.toAdmin('RAID1 no exist')
                abnormal = True
                Task.sleep(900000, "no_exist")
                continue

            if stat['state'] == 'resync':
                msg = 'RAID1 resync: %s%%' % stat['progress']
                s.log.info(msg)
                s.toAdmin(msg)
                abnormal = True
                Task.sleep(300000, "resync")
                continue

            if stat['state'] == 'recovery':
                msg = 'RAID1 recovered: %s%%' % stat['progress']
                s.log.info(msg)
                s.toAdmin(msg)
                abnormal = True
                Task.sleep(300000, "recovery")
                continue



