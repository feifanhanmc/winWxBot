#-*- coding: utf-8 -*-
from wxbot import *
from wx_xnr_es import WX_XNR_ES
from multiprocessing import Process
import ConfigParser
import socket

class WX_XNR_Bot(WXBot):
    '''
    目前仅支持通讯录里成员（个人、群组）的名称显示
    '''
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
            #目前只处理接收群消息
            if msg['msg_type_id'] == 3:
                print json.JSONEncoder().encode(msg)
#             WX_XNR_ES().save_data(msg=msg)
#             if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
#                 self.send_msg_by_uid(u'hi', msg['user']['id'])
# 


def load_config():
    cf = ConfigParser.ConfigParser()
    cf.read('wx_xnr_conf.ini')
    config = {}
    config['host'] = cf.get('wx_xnr_socket', 'host')
    config['port'] = int(cf.get('wx_xnr_socket', 'port'))
    config['DEBUG'] = cf.get('wx_xnr_bot', 'DEBUG')
    config['conf_qr'] = cf.get('wx_xnr_bot', 'conf_qr')
    config['bot_num'] = int(cf.get('wx_xnr_bot', 'bot_num'))
    return config    

def pub_msg(Bot, config):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['host'], config['port']))
    server.listen(0)
    while True:
        conn, addr = server.accept()
        print 'socket connect start at %s' % str(addr)
        data = conn.recv(1024)
        data = json.loads(data)
        if data:
            bot = Bot[data['from_bot_id']]
#             msg = {}
#             ES().save_data(msg=msg)
            print data
            print bot.send_msg(data['to_user'], data['m'])
    conn.close()  
    

def main():
    Bot = {}
    config = load_config()
    #为每一个wxbot开启一个新进程
    for i in range(config['bot_num']):
        bot_id = 'bot_' + str(i+1)
        print 'starting %s ...' % bot_id
        Bot[bot_id] = WX_XNR_Bot(bot_id=bot_id, conf_qr=config['conf_qr'], DEBUG=config['DEBUG'])
        bot = Bot[bot_id]
        if bot.run():
            Bot[bot_id] = bot
            p = Process(target=WX_XNR_Bot.proc_msg, args=(bot,))
            p.start()
    #开启所有的wxbot之后，主进程监听有没有要主动发送消息的任务
    pub_msg(Bot, config)        
        
if __name__ == '__main__':
    main()
    