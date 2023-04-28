from MonitorBase import *
import subprocess


class RoRwMonitor(MonitorBase):
    def __init__(s, hm):
        super().__init__(hm, "RoRwMonitor")

    def isRo(s):
        p = subprocess.run('mount | grep " / "', shell=True, capture_output=True, text=True)
        items = p.stdout.split()
        if items[0] == 'overlayroot':
            return True
        return False


    def do(s):
        s.abnormal = False
        while(1):
            if not s.isRo():
                s.toAdminSync('root file system is not RO. Please switch to RO')
                if not s.abnormal:
                    s.abnormal = True
                    Task.sleep(5 * 60 * 1000)
                    continue

                Task.sleep(8 * 60 * 60 * 1000)
                continue


            if s.abnormal:
                s.toAdminSync('root file system return to RO, thanks!')
                s.abnormal = False
            Task.sleep(5 * 60 * 1000)
