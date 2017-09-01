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
            print json.JSONEncoder().encode(msg)
            if msg['msg_type_id'] == 3: #目前只处理接收群消息
                groupmsg_type_id = msg['content']['type']
                groupmsg_type = ['text', 'location', 'image', 'voice', 'recommend', 'animation','share'][[0, 1, 3, 4, 5, 6, 7].index(groupmsg_type_id)]
                data = {}
                if groupmsg_type_id in [0, 1, 3, 4, 6]:
                    data['str'] = msg['content']['data']['str']
                elif groupmsg_type_id == 5:
                    data['recommend'] = msg['content']['data']['recommendinfo']
                elif groupmsg_type_id == 7 :
                    data['share'] = msg['content']['data']['share']
                wx_xnr_groupmsg = {
                    'datetime': msg['datetime'],
                    'group_id': msg['user']['id'],
                    'group_name': msg['user']['name'],
                    'speaker_id': msg['content']['user']['id'],
                    'speaker_name': msg['content']['user']['name'],
                    'msg_type': groupmsg_type,
                    'data': data
                }
                print wx_xnr_groupmsg
#                 print json.JSONEncoder().encode(msg)
#                 WX_XNR_ES().save_data(doc_type='test_group_msg', data=msg)
#             if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
#                 self.send_msg_by_uid(u'刘艺华是傻逼', msg['user']['id'])
# 


def load_config():
    cf = ConfigParser.ConfigParser()
    cf.read('wx_xnr_conf.ini')
    config = {}
    config['socket_host'] = cf.get('wx_xnr_socket', 'host')
    config['socket_port'] = int(cf.get('wx_xnr_socket', 'port'))
    config['DEBUG'] = cf.get('wx_xnr_bot', 'DEBUG')
    config['conf_qr'] = cf.get('wx_xnr_bot', 'conf_qr')
    config['bot_num'] = int(cf.get('wx_xnr_bot', 'bot_num'))
    config['es_host'] = cf.get('wx_xnr_es', 'host')
    config['es_index_name'] = cf.get('wx_xnr_es', 'index_name')
    config['test_mapping'] = eval(cf.get('wx_xnr_es', 'test_mapping'))
    return config    

def init_es(config):
    es = WX_XNR_ES(host=config['es_host'], index_name=config['es_index_name'])
    es.create_index()
#     group_msg_mapping = {
#         
#     }
#     es.put_mapping(doc_type='group_msg', mapping=group_msg_mapping)

def pub_msg(Bot, config):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((config['socket_host'], config['socket_port']))
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
    init_es(config)
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
    '''
    config = load_config()
    t = config['test_mapping']
    print type(t)
    print t['properties']
    
    
    
    config = load_config()
    with open('config.json', 'wb') as f:
        f.write(json.dumps(config))
    '''