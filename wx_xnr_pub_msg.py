# -*- coding: utf-8 -*-
import socket
import json
import ConfigParser

config ={}

def load_config():
    cf = ConfigParser.ConfigParser()
    cf.read('wx_xnr_conf.ini')
    config = {}
    config['socket_host'] = cf.get('wx_xnr_socket', 'host')
    config['socket_port'] = int(cf.get('wx_xnr_socket', 'port'))
    return config  

def socket_client(msg):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((config['host'], config['port']))
        client.send(msg)
    except Exception,e:
        print e
    finally:
        client.close()

def push_msg(from_bot_id, to_user, m):
    msg = json.dumps({'from_bot_id': from_bot_id,'to_user': to_user, 'm': m})
    socket_client(msg)

def main():
    global config
    config = load_config()
    push_msg(from_bot_id='bot_1', to_user='刘艺华', m='傻逼')

main()