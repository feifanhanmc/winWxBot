#!/usr/bin/env python
# coding: utf-8
from wxbot import *
from es import ES

class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
            print json.JSONEncoder().encode(msg)
            ES().save_data(msg=msg)
#             if msg['content']['type'] == 3:     #图片消息 
#                 self.get_msg_img(msg['msg_id'])
#             if msg['msg_type_id'] == 2 :    #文件消息
#                 pass
#             elif msg['msg_type_id'] == 3 :  #群消息
#                 if msg['content']['type'] == 0:   #文本
#                     pass
#             elif msg['msg_type_id'] == 4 :  #联系人消息
#                 if msg['content']['type'] == 0:   #文本
#                     pass
#             elif msg['msg_type_id'] == 5 :  #公众号消息
#                 pass
#             elif msg['msg_type_id'] == 6 :  #特殊账号消息
#                 pass
        



def main():
    #bot
    bot = MyWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()
