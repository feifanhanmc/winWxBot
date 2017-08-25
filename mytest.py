#!/usr/bin/env python
# coding: utf-8
from wxbot import *
from es import ES

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
            print json.JSONEncoder().encode(msg)
            ES().save_data(msg=msg)


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()
