from MonitorBase import *

class MountMonitor(MonitorBase):
    def __init__(s, hm):
        super().__init__(hm, "MountMonitor")


    def do(s):
        while(1):
            if os.path.exists('/backup/NOT_MOUNTED'):
                s.toAdminSync("/backup not mounted")
                Task.sleep(300000)

            if os.path.exists('/storage/NOT_MOUNTED'):
                s.toAdminSync("/storage not mounted")
                Task.sleep(300000)
                continue

            Task.sleep(60000)

