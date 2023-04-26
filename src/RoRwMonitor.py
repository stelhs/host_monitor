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
        abnormal = False
        while(1):
            if not s.isRo():
                s.toAdmin('root file system is not RO. Please switch to RO')
                if not abnormal:
                    abnormal = True
                    Task.sleep(5 * 60 * 1000)
                    continue

                Task.sleep(8 * 60 * 60 * 1000)
                continue


            if abnormal:
                s.toAdmin('root file system return to RO, thanks!')
                abnormal = False
            Task.sleep(5 * 60 * 1000)
