import sys, os
os.chdir(sys.path[0])

sys.path.append('sr90lib/')
sys.path.append('src/')

from math import *
import rlcompleter, readline, signal
readline.parse_and_bind('tab:complete')
import atexit

from HostMonitor import *


hm = HostMonitor()

def sigCb(signo=0, frame=None):
    print("Host monitor stopped, signo=%d" % signo)
    hm.destroy()

atexit.register(sigCb)
signal.signal(signal.SIGTERM, sigCb)

print("help:")
print("\thm")
