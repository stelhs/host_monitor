#!/usr/bin/python3

import sys, os

os.chdir(sys.path[0])

sys.path.append('sr90lib/')
sys.path.append('src/')
from TelegramClient import *
from ConfParser import *


class Conf(ConfParser):
    def __init__(s):
        super().__init__()
        s.addConfig('telegram', 'telegram.conf')

if len(sys.argv) < 2:
    print("No message")
    exit(1)

msg = sys.argv[1]
if not msg:
    print("message is empty")
    exit(1)

conf = Conf()
tc = TelegramClient(conf.telegram)
tc.sendToChatSync('stelhs', "sr90home: %s" % msg)



