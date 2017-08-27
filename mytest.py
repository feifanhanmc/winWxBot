#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Pool
import multiprocessing

from es import ES
from wxbot import *


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
#             print json.JSONEncoder().encode(msg)
            ES().save_data(msg=msg)
            if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
                self.send_msg_by_uid(u'hi', msg['user']['id'])

def run_bot():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'
    if bot.run():
        bot.proc_msg()
    
        
def main():
    bot_num = 2
    for i in range(bot_num):
        print 'bot %s ...' % str(i+1)
        p = multiprocessing.Process(target = run_bot)
        p.start()


if __name__ == '__main__':
    main()
