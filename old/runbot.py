#!/usr/bin/env python
#-*- coding: utf-8 -*-
from wxbot import *
from multiprocessing import Process
import socket
from es import ES



class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
#             print json.JSONEncoder().encode(msg)
            ES().save_data(msg=msg)
#             if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
#                 self.send_msg_by_uid(u'hi', msg['user']['id'])
# 

 

def pub_msg(Bot):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 6667))
    server.listen(0)
    while True:
        conn, addr = server.accept()
        data = conn.recv(1024)
        data = json.loads(data)
        if data:
            bot = Bot[data['from_bot_id']]
#             msg = {}
#             ES().save_data(msg=msg)
            bot.send_msg(data['to_ser'], data['m'])
    conn.close()  
    

def main():
    Bot = {}
    bot_num = 2
    #为每一个wxbot开启一个新进程
    for i in range(bot_num):
        bot_id = 'bot' + str(i+1)
        print bot_id + '...'
        Bot[bot_id] = MyWXBot(bot_id)
        bot = Bot[bot_id]
        
        bot.DEBUG = True
        bot.conf['qr'] = 'png'
         
        if bot.run():
            Bot[bot_id] = bot
            p = Process(target=MyWXBot.proc_msg, args=(bot,))
            p.start()
    
    pub_msg(Bot)        
        
if __name__ == '__main__':
    main()
