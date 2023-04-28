from MonitorBase import *
import subprocess, re

class FreeSpaceMonitor(MonitorBase):
    def __init__(s, hm):
        super().__init__(hm, "FreeSpaceMonitor")
        s.conf = s.hm.conf.freeSpace


    def df(s):
        p = subprocess.run('df -h', shell=True, capture_output=True, text=True)
        rows = p.stdout.split('\n')
        table = []
        for row in rows[1:]:
            cols = row.split()
            if len(cols) < 6:
                continue
            table.append({'dev': cols[0],
                          'size': cols[1],
                          'used': cols[2],
                          'avail': cols[3],
                          'use': int(re.findall('(\d+)', cols[4])[0]),
                          'mPoint': cols[5]})
        return table


    def do(s):
        while(1):
            tb = s.df()
            for mp in s.conf['mountPoints']:
                for row in tb:
                    if row['mPoint'] == mp:
                        if row['use'] >= s.conf['maxUsed']:
                            s.toAdminSync("No free space on %s. free: %s" % (
                                      mp, row['avail']))

            Task.sleep(30 * 60 * 1000)

