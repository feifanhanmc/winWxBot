#-*- coding: utf-8 -*-
from multiprocessing import Process
import socket
import threading
import time
from wx_xnr_es import WX_XNR_ES
from wxbot import *

config = {}
Bot = {}

class WX_XNR_Bot(WXBot):
    '''
    目前仅支持通讯录里成员（个人、群组）的名称显示
    '''
    def handle_msg_all(self, msg):
        if not msg['msg_type_id'] in (0, 1, 99):    #过滤掉无意义的消息
            if msg['msg_type_id'] == 3: #目前只处理接收群消息
                groupmsg_type_id = msg['content']['type']
                if groupmsg_type_id in [0, 1, 3, 4, 5, 6, 7, 8, 20]:   #目前只处理群内部这些类型的消息
                    groupmsg_type = ['text', 'location', 'image', 'voice', 'recommend', 'animation', 'share', 'rename'][[0, 1, 3, 4, 5, 6, 7, 20].index(groupmsg_type_id)]
                    msgid = msg['msg_id']
                    data = {}
                    if groupmsg_type == 'rename' :   #更改群名称类型的消息, 由于这类消息属于系统通知类型的。所以不予存储，而是直接进行刷新等后台操作。
                        group_name = msg['user']['name']
                        new_group_name = msg['content']['data']['str']
                    else:   #存储联系人发出的消息
                        if groupmsg_type == 'image' :  #图片类型的消息要进行保存。data['str']保存的是图片的本地存储地址
                                data['str'] = self.get_msg_img(msgid)
                        elif groupmsg_type == 'voice' :  #语音类型的消息要进行保存。data['str']保存的是语音的本地存储地址
                                data['str'] = self.get_voice(msgid)
                        elif groupmsg_type == 'recommend' :    #名片类型的消息
                            data['recommend'] = msg['content']['data']['recommendinfo']
                        elif groupmsg_type == 'share' :    #分享类型的消息
                            data['share'] = msg['content']['data']['share']
                        else:
                            data['str'] = msg['content']['data']['str']
                        wx_xnr_groupmsg = {
                            'timestamp': msg['timestamp'],
                            'group_id': msg['user']['id'],
                            'group_name': msg['user']['name'],
                            'speaker_id': msg['content']['user']['id'],
                            'speaker_name': msg['content']['user']['name'],
                            'msg_type': groupmsg_type,
                            'data': data
                        }
                        WX_XNR_ES(self.es_host, self.es_index_name).save_data(doc_type='groupmsg', data=wx_xnr_groupmsg)

def load_config():
    with open('wx_xnr_conf.json', 'r') as f:
        return json.load(f)

def init_es():
    es = WX_XNR_ES(host=config['es_host'], index_name=config['es_index_name'])
    es.create_index()
    es.put_mapping(doc_type='groupmsg', mapping=config['wx_xnr_groupmsg_mapping'])

def tcplink(conn, addr):
    print 'Accept new connection from %s:%s...'  % addr
    while True:
        data = conn.recv(1024)
        if data:
            data = json.loads(data)
            bot = Bot[data['from_bot_id']]
            group_id = bot.get_user_id(data['to_group_name'])
            if group_id:
                if bot.send_msg_by_uid(word=data['m'], dst=group_id):
                    wx_xnr_groupmsg = {
                        'timestamp': int(time.time()),
                        'group_id': group_id,
                        'group_name': data['to_group_name'],
                        'speaker_id': bot.bot_id,
                        'speaker_name': bot.bot_id,
                        'msg_type': 'text',
                        'data': {
                            'str': data['m']
                        }
                    }
                    WX_XNR_ES(bot.es_host, bot.es_index_name).save_data(doc_type='groupmsg', data=wx_xnr_groupmsg)
                    print 'Your message was sent successfully.'
        else:
            break
    conn.close()  
    print 'Connection from %s:%s closed.' % addr
    
def pub_msg():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['socket_host'], config['socket_port']))
    server.listen(5)    #等待连接的最大数量为5
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=tcplink, args=(conn, addr))
        t.start()
    
def main():
    global config
    global Bot
    config = load_config()
    init_es()
    #为每一个wxbot开启一个新进程
    for i in range(config['bot_num']):
        bot_id = 'bot_' + str(i+1)
        print 'starting %s ...' % bot_id
        Bot[bot_id] = WX_XNR_Bot(bot_id=bot_id, conf_qr=config['conf_qr'], DEBUG=config['DEBUG'], es_host=config['es_host'], es_index_name=config['es_index_name'])
        bot = Bot[bot_id]
        if bot.run():
            Bot[bot_id] = bot
            p = Process(target=WX_XNR_Bot.proc_msg, args=(bot,))
            p.start()
    #开启所有的wxbot之后，主进程监听有没有要主动发送消息的任务
    pub_msg()     
        
if __name__ == '__main__':
    main()












