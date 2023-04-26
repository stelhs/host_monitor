from Task import *


class MonitorBase():
    def __init__(s, hm, name):
        s.hm = hm
        s.name = name
        s.task = Task(name, s.do, s.onTaskStopped)
        s.log = Syslog(name)


    def toAdmin(s, msg):
        s.hm.toAdmin("%s: %s" % (s.name, msg))

    def toAdminSync(s, msg):
        s.hm.toAdminSync("%s: %s" % (s.name, msg))


    def onTaskStopped(s):
        s.toAdmin("stopped")
        s.log.info("started")


    def start(s):
        s.task.start()
        s.toAdmin("started")
        s.log.info("started")


    def stop(s):
        s.task.stop()
        s.log.info("call stop")


    def destroy(s):
        s.stop()
        print('destroyed %s' % s.name)
