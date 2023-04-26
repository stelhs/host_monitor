from Syslog import *
from ConfHostMonitor import *
from TelegramClient import *
from MdMonitor import *
from MountMonitor import *
from FreeSpaceMonitor import *


class HostMonitor():
    def __init__(s):
        s.log = Syslog("HostMonitor")
        s.conf = ConfHostMonitor()
        s.tc = TelegramClient(s.conf.telegram)
        Task.setErrorCb(s.taskExceptionHandler)
        s.md = MdMonitor(s)
        s.mm = MountMonitor(s)
        s.fsm = FreeSpaceMonitor(s)

        s.md.start()
        s.mm.start()
        s.fsm.start()


    def toAdmin(s, msg):
        s.tc.sendToChat('stelhs', "sr90home: %s" % msg)


    def toAdminSync(s, msg):
        s.tc.sendToChatSync('stelhs', "sr90home: %s" % msg)


    def taskExceptionHandler(s, task, errMsg):
        s.toAdmin("task '%s' error:\n%s" % (task.name(), errMsg))


    def destroy(s):
        s.md.destroy()
        s.mm.destroy()
        s.fsm.destroy()
        print('destroyed HostMonitor')
        Task.sleep(1000)
        s.toAdminSync("destroyed")

