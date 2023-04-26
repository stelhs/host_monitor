from ConfParser import *

class ConfHostMonitor(ConfParser):
    def __init__(s):
        super().__init__()
        s.addConfig('telegram', 'telegram.conf')
        s.addConfig('freeSpace', 'freeSpace.conf')



